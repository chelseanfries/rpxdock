#! /home/sheffler/.conda/envs/rpxdock/bin/python

import logging, itertools, concurrent, tqdm, rpxdock as rp
import numpy as np

def get_rpxdock_args():
   arg = rp.options.get_cli_args()
   if not arg.architecture: raise ValueError("architecture must be specified")
   return arg

def get_spec(arch):
   arch = arch.upper()
   if arch.startswith('P'):
      sym = arch.split('_')[0]
      component_nfold = arch.split('_')[1]
      ismirror = sym[-1] == 'M'
      if len(component_nfold) == 1 and ismirror:
         spec = rp.search.DockSpec1CompMirrorLayer(arch)
      elif len(component_nfold) == 1:
         spec = rp.search.DockSpec1CompLayer(arch)
      elif len(component_nfold) == 2:
         spec = rp.search.DockSpec2CompLayer(arch)
      elif len(component_nfold) == 3:
         spec = rp.search.DockSpec3CompLayer(arch)
      else:
         raise ValueError('number of conponents must be 1, 2 or 3')
   elif len(arch) == 2 or (arch[0] == 'D' and arch[2] == '_'):
      spec = rp.search.DockSpec1CompCage(arch)
   else:
      spec = rp.search.DockSpec2CompCage(arch)
   return spec

## All dock_cyclic, dock_onecomp, and dock_multicomp do similar things
def dock_cyclic(hscore, inputs, architecture, **kw):
   ## bunch is a dictionary of things
   arg = rp.Bunch(kw)
   ## bodies hold all pose info and axis intersect info
   bodies = [rp.Body(inp, **arg) for inp in arg.inputs1]

   ## start the parallel processes
   exe = concurrent.futures.ProcessPoolExecutor
   # exe = rp.util.InProcessExecutor
   with exe(arg.ncpu) as pool:
      futures = list()
      # where the magic happens
      for ijob, bod in enumerate(bodies):
         futures.append(
            pool.submit(
               rp.search.make_cyclic,
               bod,
               architecture.upper(),
               hscore,
               **arg,
            ))
         futures[-1].ijob = ijob
      result = [None] * len(futures)
      for f in tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
         result[f.ijob] = f.result()
   result = rp.concat_results(result)

   # result = rp.search.make_cyclic(body, architecture.upper(), hscore, **arg)

   return result

def dock_onecomp(hscore, **kw):
   arg = rp.Bunch(kw)
   # for 1comp, len(arch) == 2
   spec = get_spec(arg.architecture)
   # double normal resolution, cuz why not?
   # mirrorlayer for 1comp xtals and stuff with P architectures
   if arg.docking_method == 'grid':
      cart = np.arange(-300.5, 300.6)
      ang = np.arange(-180/int(arch[1]), 180/int(arch[1])+0.1, 1)
      if arg.flip_components is None:
         sampler = rp.sampling.grid_sym_axis(cart, ang, axis = spec.axis)
      else:
         sampler = rp.sampling.grid_sym_axis(cart, ang, axis = spec.axis, flip = arg.flip_components)
      search = rp.grid_search
   else:
      if spec.type == 'mirrorlayer':
         sampler = rp.sampling.hier_mirror_lattice_sampler(spec, resl=10, angresl=10, **arg)
      else:
         sampler = rp.sampling.hier_axis_sampler(spec.nfold, lb=0, ub=100, resl=5, angresl=5,
                                              axis=spec.axis, flipax=spec.flip_axis)
   
      search=rp.hier_search

   # pose info and axes that intersect
   bodies = [rp.Body(inp, **arg) for inp in arg.inputs1]

   exe = concurrent.futures.ProcessPoolExecutor
   # exe = rp.util.InProcessExecutor
   with exe(arg.ncpu) as pool:
      futures = list()
      for ijob, bod in enumerate(bodies):
         futures.append(
            pool.submit(
               rp.search.make_onecomp,
               bod,
               spec,
               hscore,
               search,
               sampler,
               **arg,
            ))
         futures[-1].ijob = ijob
      result = [None] * len(futures)
      for f in tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
         result[f.ijob] = f.result()
   
   result = rp.concat_results(result)
   return result
   # result = rp.search.make_onecomp(bodyC3, spec, hscore, rp.hier_search, sampler, **arg)

def dock_multicomp(hscore, **kw):
   arg = rp.Bunch(kw)
   spec = get_spec(arg.architecture)
   sampler = rp.sampling.hier_multi_axis_sampler(spec, **arg)
   logging.info(f'num base samples {sampler.size(0):,}')

   bodies = [[rp.Body(fn, **arg) for fn in inp] for inp in arg.inputs]
   assert len(bodies) == spec.num_components

   exe = concurrent.futures.ProcessPoolExecutor
   # exe = rp.util.InProcessExecutor
   with exe(arg.ncpu) as pool:
      futures = list()
      for ijob, bod in enumerate(itertools.product(*bodies)):
         futures.append(
            pool.submit(
               rp.search.make_multicomp,
               bod,
               spec,
               hscore,
               rp.hier_search,
               sampler,
               **arg,
            ))
         futures[-1].ijob = ijob
      result = [None] * len(futures)
      for f in tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
         result[f.ijob] = f.result()
   result = rp.concat_results(result)
   return result

def main():
   # What gets all the shit done
   arg = get_rpxdock_args()
   logging.info(f'weights: {arg.wts}')

   hscore = rp.CachedProxy(rp.RpxHier(arg.hscore_files, **arg))
   arch = arg.architecture

   # TODO commit to master AK
   #sym, comp = arch.split('_')

   # TODO: redefine archs WHS or others with a monster list of if statements
   if arch.startswith('C'):
      result = dock_cyclic(hscore, **arg)
   elif len(arch) == 2 or (arch[0] == 'D' and arch[2] == '_'):
      result = dock_onecomp(hscore, **arg)
   else:
      result = dock_multicomp(hscore, **arg)

   print(result)
   if arg.dump_pdbs:
      result.dump_pdbs_top_score(hscore=hscore, **arg)
      result.dump_pdbs_top_score_each(hscore=hscore, **arg)
   if not arg.suppress_dump_results:
      rp.util.dump(result, arg.output_prefix + '_Result.pickle')

if __name__ == '__main__':
   main()
