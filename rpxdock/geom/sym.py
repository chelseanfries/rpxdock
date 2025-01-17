import numpy as np, rpxdock as rp
from rpxdock import homog as hm

tetrahedral_frames = np.load(rp.data.datadir + "/tetrahedral_frames.pickle", allow_pickle=True)
octahedral_frames = np.load(rp.data.datadir + "/octahedral_frames.pickle", allow_pickle=True)
icosahedral_frames = np.load(rp.data.datadir + "/icosahedral_frames.pickle", allow_pickle=True)

def symframes(sym, pos=None, axis=[0,0,1], **kw):
   kw = rp.Bunch(kw)
   if isinstance(sym, np.ndarray):
      assert len(sym) == 1
      sym = sym[0]
   if isinstance(sym, (int, np.int32, np.int64, np.uint32, np.uint64)):
      sym = int(sym)
   if isinstance(sym, int) or sym.startswith("C"):
      if not isinstance(sym, int): sym = int(sym[1:])
      return np.array(list(hm.hrot(axis, np.arange(sym) / sym * 360)))
   elif sym.startswith("D"):
      assert np.allclose(axis, [0, 0, 1])
      if '_' not in sym:
         nsym = int(sym[1:])
      else:
         nsym = int(sym[1:sym.find('_')])
      frames_up = list(hm.hrot([0, 0, 1], np.arange(nsym) / nsym * 360))
      frames_dn = list(hm.hrot([1, 0, 0], np.pi) @ frames_up)
      return np.array(frames_up + frames_dn)
   elif sym.startswith("T"):
      return tetrahedral_frames
   elif sym.startswith("O"):
      return octahedral_frames
   elif sym.startswith("I"):
      return icosahedral_frames
   elif sym.startswith('H'):
      assert len(sym) == 2
      nfold = int(sym[1])
      frames = [np.eye(4)]
      for i in range(int(np.floor(kw.symframe_num_helix_repeats / 2))):
         frames.append(pos @ frames[-1])
      frames += [np.linalg.inv(x) for x in frames[1:]]
      return np.array(frames)
   elif sym == 'P6_632':
      c6 = hm.hrot(axis, np.arange(6) / 6 * 360)
      c3 = hm.hrot(axis, np.arange(3) / 3 * 360, center=[pos[1, 0, 3], pos[1, 1, 3], 0])
      c2 = hm.hrot(axis, np.arange(2) / 2 * 360, center=[pos[2, 0, 3], pos[2, 1, 3], 0])
      frames = c6[None, None, :] @ c3[None, :, None] @ c2[:, None, None]
      return frames.reshape(-1, 4, 4)

   elif sym == 'P6_32':
      c3 = hm.hrot(axis, np.arange(3) / 3 * 360)
      c2 = hm.hrot(axis, np.arange(2) / 2 * 360, center=[pos[1, 0, 3], pos[1, 1, 3], 0])
      #center inputs are 3 x,y,z, each list should be something like position, spin, offset (idk for sure)
      #if you change the center of c2, c3 spins to compensate for change

      frames = c3[:, None] @ c2[None, :]
      #doesnt know what nfold is yet
      return frames.reshape(-1, 4, 4)

   elif sym == 'P6_33':
      c3 = hm.hrot(axis, np.arange(3) / 3 * 360)
      c3b = hm.hrot(axis, np.arange(3) / 3 * 360, center=[pos[1, 0, 3], pos[1, 1, 3], 0])
      frames = c3[:, None] @ c3b[None, :]
      return frames.reshape(-1, 4, 4)

   elif sym == 'P6_63':
      c6 = hm.hrot(axis, np.arange(6) / 6 * 360)
      c3 = hm.hrot(axis, np.arange(3) / 3 * 360, center=[pos[1, 0, 3], pos[1, 1, 3], 0])
      frames = c6[:, None] @ c3[None, :]
      return frames.reshape(-1, 4, 4)

   elif sym == 'P6_62':
      c6 = hm.hrot(axis, np.arange(6) / 6 * 360)
      c2 = hm.hrot(axis, np.arange(2) / 2 * 360, center=[pos[1, 0, 3], pos[1, 1, 3], 0])
      frames = c6[:, None] @ c2[None, :]
      return frames.reshape(-1, 4, 4)

   elif sym == 'P4_42':
      c4 = hm.hrot(axis, np.arange(4) / 4 * 360)
      c2 = hm.hrot(axis, np.arange(2) / 2 * 360, center=[pos[1, 0, 3], pos[1, 1, 3], 0])
      frames = c4[:, None] @ c2[None, :]
      return frames.reshape(-1, 4, 4)

   elif sym == 'P4_44':
      c4 = hm.hrot(axis, np.arange(4) / 4 * 360)
      c4b = hm.hrot(axis, np.arange(4) / 4 * 360, center=[pos[1, 0, 3], pos[1, 1, 3], 0])
      frames = c4[:, None] @ c4b[None, :]
      return frames.reshape(-1, 4, 4)

   elif sym.startswith('F_32'):
      c3 = hm.hrot(axis, np.arange(3) / 3 * 360)
      if sym.endswith('4'):
         axis2 = [1, 0, 0]
      if sym.endswith('6'):
         axis2 = [1.7320508075688767, 0, 1]
      if sym.endswith('8'):
         axis2 = [1, 0, 1]
      if sym.endswith('10'):
         axis2 = [0.7265425280053609, 0, 1]
      if sym.endswith('12'):
         axis2 = [0.5773502691896257, 0, 1]
      if sym.endswith('14'):
         axis2 = [0.48157461880752883, 0, 1]
      if sym.endswith('16'):
         axis2 = [0.41421356237309503, 0, 1]
      if sym.endswith('18'):
         axis2 = [0.36397023426620234, 0, 1]
      if sym.endswith('20'):
         axis2 = [0.3249196962329063, 0, 1]
      if sym.endswith('22'):
         axis2 = [0.2936264929383669, 0, 1],
      if sym.endswith('24'):
         axis2 = [0.2679491924311227, 0, 1]
      if sym.endswith('26'):
         axis2 = [0.24647786303197738, 0, 1]
      if sym.endswith('28'):
         axis2 = [0.22824347439015003, 0, 1]
      if sym.endswith('30'):
         axis2 = [0.21255656167002213, 0, 1]
      if sym.endswith('32'):
         axis2 = [0.198912367379658, 0, 1]
      if sym.endswith('34'):
         axis2 = [0.18693239710797724, 0, 1]
      if sym.endswith('36'):
         axis2 = [0.17632698070846498, 0, 1]
      c2 = hm.hrot(axis2, np.arange(2) / 2 * 360,  center=[pos[1, 0, 3], pos[1, 1, 3], pos[1, 2, 3]])
      frames = c3[:, None] @ c2[None, :]
      return frames.reshape(-1, 4, 4)

   elif sym.startswith('F_42'):
      c4 = hm.hrot(axis, np.arange(4) / 4 * 360)
      if sym.endswith('4'):
         axis2 = [1, 0, 0]
      if sym.endswith('6'):
         axis2 = [1.7320508075688767, 0, 1]
      if sym.endswith('8'):
         axis2 = [1, 0, 1]
      if sym.endswith('10'):
         axis2 = [0.7265425280053609, 0, 1]
      if sym.endswith('12'):
         axis2 = [0.5773502691896257, 0, 1]
      if sym.endswith('14'):
         axis2 = [0.48157461880752883, 0, 1]
      if sym.endswith('16'):
         axis2 = [0.41421356237309503, 0, 1]
      if sym.endswith('18'):
         axis2 = [0.36397023426620234, 0, 1]
      if sym.endswith('20'):
         axis2 = [0.3249196962329063, 0, 1]
      if sym.endswith('22'):
         axis2 = [0.2936264929383669, 0, 1],
      if sym.endswith('24'):
         axis2 = [0.2679491924311227, 0, 1]
      if sym.endswith('26'):
         axis2 = [0.24647786303197738, 0, 1]
      if sym.endswith('28'):
         axis2 = [0.22824347439015003, 0, 1]
      if sym.endswith('30'):
         axis2 = [0.21255656167002213, 0, 1]
      if sym.endswith('32'):
         axis2 = [0.198912367379658, 0, 1]
      if sym.endswith('34'):
         axis2 = [0.18693239710797724, 0, 1]
      if sym.endswith('36'):
         axis2 = [0.17632698070846498, 0, 1]
      c2 = hm.hrot(axis2, np.arange(2) / 2 * 360,  center=[pos[1, 0, 3], pos[1, 1, 3], pos[1, 2, 3]])
      frames = c4[:, None] @ c2[None, :]
      return frames.reshape(-1, 4, 4)
   elif sym == 'P4M_4':
      c4a = hm.hrot(axis, np.arange(4) / 4 * 360)
      c4b = hm.hrot(axis, np.arange(4) / 4 * 360, center=[pos[0, 3], pos[1, 3], 0])
      c2 = hm.hrot(axis, np.arange(2) / 2 * 360, center=[pos[0, 3] / 2, pos[1, 3] / 2, 0])
      frames = c4a[None, None, :] @ c2[None, :, None] @ c4b[:, None, None]
      return frames.reshape(-1, 4, 4)
   elif sym.startswith("AXEL_"):
      nfold = int(sym.split("_")[1])
      return np.array(list(hm.hrot(axis, np.arange(nfold) / nfold * 360)))
   else:
      raise NotImplementedError

frames = dict(T=tetrahedral_frames, O=octahedral_frames, I=icosahedral_frames)

tetrahedral_axes = {
   2: hm.hnormalized([1, 0, 0]),
   3: hm.hnormalized([1, 1, 1]),
   33: hm.hnormalized([1, 1, -1]),
}  # other c3
octahedral_axes = {
   2: hm.hnormalized([1, 1, 0]),
   3: hm.hnormalized([1, 1, 1]),
   4: hm.hnormalized([1, 0, 0]),
}
icosahedral_axes = {
   2: hm.hnormalized([1, 0, 0]),
   3: hm.hnormalized([0.934172, 0.000000, 0.356822]),
   5: hm.hnormalized([0.850651, 0.525731, 0.000000]),
}
dihedral_axes = {
   2: hm.hnormalized([1, 0, 0]),
   22: hm.hnormalized([0, 0, 1]),
   3: hm.hnormalized([0, 0, 1]),
   4: hm.hnormalized([0, 0, 1]),
   5: hm.hnormalized([0, 0, 1]),
   6: hm.hnormalized([0, 0, 1]),
   7: hm.hnormalized([0, 0, 1]),
   8: hm.hnormalized([0, 0, 1]),
   9: hm.hnormalized([0, 0, 1]),
   10: hm.hnormalized([0, 0, 1]),
   11: hm.hnormalized([0, 0, 1]),
   12: hm.hnormalized([0, 0, 1]),
}
axes = dict(T=tetrahedral_axes, O=octahedral_axes, I=icosahedral_axes, D=dihedral_axes)
for i in range(2, 13):
   axes[f'D{i}'] = axes['D']

to_neighbor_olig = dict(
   T={
      2: frames["T"][2],
      3: frames["T"][1],
      33: frames["T"][1]
   },
   O={
      2: frames["O"][2],
      3: frames["O"][1],
      4: frames["O"][1]
   },
   I={
      2: frames["I"][1],
      3: frames["I"][1],
      5: frames["I"][2]
   },
   D22={
      2: hm.hrot([0, 0, 1], np.pi),
      22: hm.hrot([1, 0, 0], np.pi),
   },
   D2={
      2: hm.hrot([0, 1, 0], np.pi),
   },
)

axes_second = {s: {k: to_neighbor_olig[s][k] @ v for k, v in axes[s].items()} for s in "TOI"}

axes_second['D22'] = {
   2: to_neighbor_olig['D22'][2] @ dihedral_axes[2],
   22: to_neighbor_olig['D22'][22] @ dihedral_axes[22],
}
axes_second['D2'] = {
   2: to_neighbor_olig['D2'][2] @ dihedral_axes[2],
}

for i in range(3, 13):
   to_neighbor_olig[f'D{i}'] = {
      2: hm.hrot([0, 0, 1], 2 * np.pi / i),
      i: hm.hrot([1, 0, 0], np.pi),
   }
   to_neighbor_olig[f'D{i}2'] = to_neighbor_olig[f'D{i}']

   axes_second[f'D{i}'] = {
      2: to_neighbor_olig[f'D{i}'][2] @ dihedral_axes[2],
      i: to_neighbor_olig[f'D{i}'][i] @ dihedral_axes[i],
   }
   axes_second[f'D{i}2'] = axes_second[f'D{i}']

# for i in range(2, 13):
#    axes[f'D{i}'] = axes['D']
#    axes_second[f'D{i}'] = axes_second['D']

# tetrahedral_frames = np.array(
# [
# (
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, -0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (-0.000000, +0.000000, +1.000000, +0.000000),
# (+1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -1.000000, +0.000000, +0.000000),
# (-0.000000, -0.000000, -1.000000, +0.000000),
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (+0.000000, -0.000000, -1.000000, +0.000000),
# (-1.000000, +0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, +0.000000, +1.000000, +0.000000),
# (+1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (-1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, -0.000000, -1.000000, +0.000000),
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (+0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -0.000000, -1.000000, +0.000000),
# (-1.000000, -0.000000, -0.000000, +0.000000),
# (-0.000000, +1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, +0.000000, +1.000000, +0.000000),
# (-1.000000, +0.000000, -0.000000, +0.000000),
# (-0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, -0.000000, -0.000000, +0.000000),
# (-0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, +0.000000, -0.000000, +0.000000),
# (-0.000000, -1.000000, +0.000000, +0.000000),
# (-0.000000, +0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# ]
# )
#
# octahedral_frames = np.array(
# [
# (
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (-0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (+1.000000, -0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (-0.000000, +1.000000, +0.000000, +0.000000),
# (-1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+1.000000, -0.000000, -0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (+1.000000, -0.000000, -0.000000, +0.000000),
# (-0.000000, -1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (-0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (-1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (-0.000000, -0.000000, +1.000000, +0.000000),
# (-1.000000, -0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, -1.000000, -0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (+1.000000, -0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +0.000000, -1.000000, +0.000000),
# (-0.000000, -1.000000, -0.000000, +0.000000),
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (-0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, -0.000000, -0.000000, +0.000000),
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (-0.000000, -0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (-1.000000, -0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# ]
# )
#
# icosahedral_frames = np.array(
# [
# (
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, +0.309017, +0.500000, +0.000000),
# (+0.309017, +0.500000, -0.809017, +0.000000),
# (-0.500000, +0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, +0.309017, +0.500000, +0.000000),
# (-0.309017, -0.500000, +0.809017, +0.000000),
# (+0.500000, -0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, +0.309017, -0.500000, +0.000000),
# (+0.309017, +0.500000, +0.809017, +0.000000),
# (+0.500000, -0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, +0.309017, -0.500000, +0.000000),
# (-0.309017, -0.500000, -0.809017, +0.000000),
# (-0.500000, +0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, -0.309017, +0.500000, +0.000000),
# (+0.309017, -0.500000, -0.809017, +0.000000),
# (+0.500000, +0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, -0.309017, +0.500000, +0.000000),
# (-0.309017, +0.500000, +0.809017, +0.000000),
# (-0.500000, -0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, -0.309017, -0.500000, +0.000000),
# (+0.309017, -0.500000, +0.809017, +0.000000),
# (-0.500000, -0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, -0.309017, -0.500000, +0.000000),
# (-0.309017, +0.500000, -0.809017, +0.000000),
# (+0.500000, +0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, +0.809017, +0.309017, +0.000000),
# (+0.809017, -0.309017, -0.500000, +0.000000),
# (-0.309017, +0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, +0.809017, +0.309017, +0.000000),
# (-0.809017, +0.309017, +0.500000, +0.000000),
# (+0.309017, -0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, +0.809017, -0.309017, +0.000000),
# (+0.809017, -0.309017, +0.500000, +0.000000),
# (+0.309017, -0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, +0.809017, -0.309017, +0.000000),
# (-0.809017, +0.309017, -0.500000, +0.000000),
# (-0.309017, +0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, -0.809017, +0.309017, +0.000000),
# (+0.809017, +0.309017, -0.500000, +0.000000),
# (+0.309017, +0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, -0.809017, +0.309017, +0.000000),
# (-0.809017, -0.309017, +0.500000, +0.000000),
# (-0.309017, -0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, -0.809017, -0.309017, +0.000000),
# (+0.809017, +0.309017, +0.500000, +0.000000),
# (-0.309017, -0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, -0.809017, -0.309017, +0.000000),
# (-0.809017, -0.309017, -0.500000, +0.000000),
# (+0.309017, +0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, +0.500000, +0.809017, +0.000000),
# (+0.500000, -0.809017, +0.309017, +0.000000),
# (+0.809017, +0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, +0.500000, +0.809017, +0.000000),
# (-0.500000, +0.809017, -0.309017, +0.000000),
# (-0.809017, -0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, +0.500000, -0.809017, +0.000000),
# (+0.500000, -0.809017, -0.309017, +0.000000),
# (-0.809017, -0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, +0.500000, -0.809017, +0.000000),
# (-0.500000, +0.809017, +0.309017, +0.000000),
# (+0.809017, +0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, -0.500000, +0.809017, +0.000000),
# (+0.500000, +0.809017, +0.309017, +0.000000),
# (-0.809017, +0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, -0.500000, +0.809017, +0.000000),
# (-0.500000, -0.809017, -0.309017, +0.000000),
# (+0.809017, -0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, -0.500000, -0.809017, +0.000000),
# (+0.500000, +0.809017, -0.309017, +0.000000),
# (+0.809017, -0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, -0.500000, -0.809017, +0.000000),
# (-0.500000, -0.809017, +0.309017, +0.000000),
# (-0.809017, +0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+1.000000, -0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (+1.000000, -0.000000, -0.000000, +0.000000),
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (-0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (-1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -1.000000, +0.000000, +0.000000),
# (-0.000000, -0.000000, -1.000000, +0.000000),
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -0.000000, -1.000000, +0.000000),
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -0.000000, -1.000000, +0.000000),
# (-1.000000, -0.000000, -0.000000, +0.000000),
# (-0.000000, +1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, -0.000000, +0.000000, +0.000000),
# (-0.000000, +1.000000, +0.000000, +0.000000),
# (-0.000000, -0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, +0.309017, +0.500000, +0.000000),
# (+0.309017, -0.500000, +0.809017, +0.000000),
# (+0.500000, +0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, +0.309017, +0.500000, +0.000000),
# (-0.309017, +0.500000, -0.809017, +0.000000),
# (-0.500000, -0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, +0.309017, -0.500000, +0.000000),
# (+0.309017, -0.500000, -0.809017, +0.000000),
# (-0.500000, -0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, +0.309017, -0.500000, +0.000000),
# (-0.309017, +0.500000, +0.809017, +0.000000),
# (+0.500000, +0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, -0.309017, +0.500000, +0.000000),
# (+0.309017, +0.500000, +0.809017, +0.000000),
# (-0.500000, +0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, -0.309017, +0.500000, +0.000000),
# (-0.309017, -0.500000, -0.809017, +0.000000),
# (+0.500000, -0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, -0.309017, -0.500000, +0.000000),
# (+0.309017, +0.500000, -0.809017, +0.000000),
# (+0.500000, -0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, -0.309017, -0.500000, +0.000000),
# (-0.309017, -0.500000, +0.809017, +0.000000),
# (-0.500000, +0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, +0.809017, +0.309017, +0.000000),
# (+0.809017, +0.309017, +0.500000, +0.000000),
# (+0.309017, +0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, +0.809017, +0.309017, +0.000000),
# (-0.809017, -0.309017, -0.500000, +0.000000),
# (-0.309017, -0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, +0.809017, -0.309017, +0.000000),
# (+0.809017, +0.309017, -0.500000, +0.000000),
# (-0.309017, -0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, +0.809017, -0.309017, +0.000000),
# (-0.809017, -0.309017, +0.500000, +0.000000),
# (+0.309017, +0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, -0.809017, +0.309017, +0.000000),
# (+0.809017, -0.309017, +0.500000, +0.000000),
# (-0.309017, +0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, -0.809017, +0.309017, +0.000000),
# (-0.809017, +0.309017, -0.500000, +0.000000),
# (+0.309017, -0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, -0.809017, -0.309017, +0.000000),
# (+0.809017, -0.309017, -0.500000, +0.000000),
# (+0.309017, -0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, -0.809017, -0.309017, +0.000000),
# (-0.809017, +0.309017, +0.500000, +0.000000),
# (-0.309017, +0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, +0.500000, +0.809017, +0.000000),
# (+0.500000, +0.809017, -0.309017, +0.000000),
# (-0.809017, +0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, +0.500000, +0.809017, +0.000000),
# (-0.500000, -0.809017, +0.309017, +0.000000),
# (+0.809017, -0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, +0.500000, -0.809017, +0.000000),
# (+0.500000, +0.809017, +0.309017, +0.000000),
# (+0.809017, -0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, +0.500000, -0.809017, +0.000000),
# (-0.500000, -0.809017, -0.309017, +0.000000),
# (-0.809017, +0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, -0.500000, +0.809017, +0.000000),
# (+0.500000, -0.809017, -0.309017, +0.000000),
# (+0.809017, +0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, -0.500000, +0.809017, +0.000000),
# (-0.500000, +0.809017, +0.309017, +0.000000),
# (-0.809017, -0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, -0.500000, -0.809017, +0.000000),
# (+0.500000, -0.809017, +0.309017, +0.000000),
# (-0.809017, -0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, -0.500000, -0.809017, +0.000000),
# (-0.500000, +0.809017, -0.309017, +0.000000),
# (+0.809017, +0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# ]
# )
#
# tetrahedral_frames.dump("rpxdock/data/tetrahedral_frames.pickle")
# octahedral_frames.dump("rpxdock/data/octahedral_frames.pickle")
# icosahedral_frames.dump("rpxdock/data/icosahedral_frames.pickle")
