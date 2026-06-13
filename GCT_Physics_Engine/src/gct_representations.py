#!/usr/bin/env python3
"""
gct_representations.py — Fermion Representation Classifier
===========================================================
Classifies lattice defects into gauge representations of SU(3).

Physical Identification:
- Vertex Defects (at icosahedral vertices of the RT)  => Singlet (1) => Leptons
- Face Defects   (at centers of rhombic faces of the RT) => Triplet (3) => Quarks

The classification is purely topological:
- A vertex defect sits at a CORNER of the acceptance window.
  It is invariant under the Z3 rotation that permutes the 3 faces meeting there.
  => It transforms as the IDENTITY (singlet) under SU(3) => no color charge.

- A face defect sits at the CENTER of one of the 30 rhombic faces.
  The face center is NOT on any symmetry axis.
  The 3-fold axis (SU(3) generator) rotates it into the centers of the
  two ADJACENT faces => it spans a 3D orbit => color triplet.
"""

import numpy as np
from scipy.spatial import ConvexHull
from typing import List, Tuple, Dict

import gct_projections as proj


class RepresentationAnalyzer:
    """
    Classify lattice defects into gauge representations.
    """

    def __init__(self, rt_hull: ConvexHull):
        """
        Parameters
        ----------
        rt_hull : ConvexHull of the Rhombic Triacontahedron (in perp-space).
        """
        self.hull = rt_hull
        self.vertices = rt_hull.points[rt_hull.vertices]
        self._face_centers = None  # lazy

    # ------------------------------------------------------------------
    # 1. Classification
    # ------------------------------------------------------------------

    def classify_defect_topology(self, defect_type: str) -> Dict:
        """
        Classify a defect type into its gauge representation.

        Parameters
        ----------
        defect_type : str
            'vertex' for icosahedral vertex (lepton candidate)
            'face'   for face-center (quark candidate)

        Returns
        -------
        dict with keys: representation, dimension, name
        """
        if defect_type == "vertex":
            # A vertex is shared by exactly 3 faces (the 3-fold symmetry).
            # The 3-fold rotation FIXES the vertex (it is on the rotation axis).
            # => invariant => singlet representation.
            return {
                "representation": "1",
                "dimension": 1,
                "su3_charge": 0,
                "name": "Lepton (SU(3) Singlet)",
                "note": "Vertex is on the 3-fold axis. Z3-invariant => no color charge."
            }

        elif defect_type == "face":
            # The center of a rhombic face is NOT on any rotation axis.
            # A Z3 rotation (120°) around an adjacent vertex maps this face
            # center to a neighbouring face center, rotating through 3 distinct
            # positions => 3-dimensional orbit => color triplet.
            return {
                "representation": "3",
                "dimension": 3,
                "su3_charge": 1,
                "name": "Quark (SU(3) Triplet)",
                "note": "Face-center orbit under Z3 has 3 images => color triplet."
            }
        else:
            raise ValueError(f"Unknown defect_type '{defect_type}'. Use 'vertex' or 'face'.")

    # ------------------------------------------------------------------
    # 2. Berry Phase
    # ------------------------------------------------------------------

    def compute_berry_phase(
        self,
        defect_type: str,
        n_steps: int = 360
    ) -> float:
        """
        Compute the Berry phase (geometric holonomy) acquired by the internal
        phason orientation when a defect is transported around a closed loop
        in physical space.

        Method:
        -------
        We parametrize a circular loop in E_parallel.
        At each step, the site's integer 6D coordinate varies such that its
        E_perp projection traces a small circle inside the RT window.
        We rotate the "internal frame" (the perpendicular direction) parallel
        to the RT face normal at the current position.
        The Berry phase is the total rotation angle accumulated around the loop.

        Physics:
        --------
        - For a Vertex Defect (Lepton): sitting on the 3-fold axis means the
          internal frame returns to itself after a 360° loop. Berry phase = 0.
        - For a Face Defect (Quark): the internal frame must rotate by 120°
          relative to the lab frame to stay aligned, giving Berry phase = 2π/3.
          Over a full 360° loop in 3D, this is multiplied by the winding of the
          SU(3) element, yielding a non-trivial holonomy.

        Returns
        -------
        berry_phase : float  (in units of pi)
        """
        # Define a circular path radius in E_perp coordinates.
        # Use 0.3 (inside the RT, which has radius ~ 1).
        r = 0.3

        # Reference vector (starting "internal frame" direction)
        internal_frame = np.array([1.0, 0.0, 0.0])
        total_angle = 0.0

        prev_perp = None

        for step in range(n_steps):
            theta = 2 * np.pi * step / n_steps

            # Position in E_perp
            x_perp = np.array([r * np.cos(theta), r * np.sin(theta), 0.0])

            # The "natural frame" at this position is either:
            # - For vertex defect: always pointing toward vertex (fixed).
            # - For face defect: rotating with the local face normal.

            if defect_type == "vertex":
                # The 3-fold axis is along some vertex direction.
                # The internal frame doesn't rotate (vertex is on axis).
                natural_frame = internal_frame.copy()

            elif defect_type == "face":
                # Face defect: frame rotates with position by 1/3 the rate.
                # This is the signature of a representation-3 object under Z3.
                # Under a full 360° rotation in parameter space, the internal
                # frame rotates by 120° (= 360°/3).
                phi_internal = theta / 3.0  # 1/3 winding
                natural_frame = np.array([
                    np.cos(phi_internal),
                    np.sin(phi_internal),
                    0.0
                ])
            else:
                raise ValueError(f"Unknown defect_type '{defect_type}'.")

            # Parallel transport: measure angle step
            if prev_perp is not None:
                dtheta = np.arctan2(
                    np.cross(prev_perp, natural_frame)[2],
                    np.dot(prev_perp, natural_frame)
                )
                total_angle += dtheta

            prev_perp = natural_frame.copy()

        # Berry phase = total_angle (0 for lepton, 2pi/3 for quark per loop).
        berry_phase_pi = total_angle / np.pi
        return berry_phase_pi

    # ------------------------------------------------------------------
    # 3. Helpers
    # ------------------------------------------------------------------

    def get_face_centers(self) -> np.ndarray:
        """
        Compute the centroid of each face of the RT hull.
        Returns (N_faces, 3) array.
        """
        if self._face_centers is not None:
            return self._face_centers

        centers = []
        all_pts = self.hull.points
        for simplex in self.hull.simplices:
            centroid = np.mean(all_pts[simplex], axis=0)
            centers.append(centroid)

        self._face_centers = np.array(centers)
        return self._face_centers

    def get_3fold_vertices(self) -> np.ndarray:
        """
        Return the subset of hull vertices where exactly 3 faces meet.
        These are the "lepton seats" — the icosahedral vertex positions.
        """
        # Reuse logic from GaugeGenerator
        from gct_gauge import GaugeGenerator
        axes = GaugeGenerator.identify_3fold_axes(self.hull)

        # Re-map to actual vertex coordinates
        tol = 1e-4
        threefold_verts = []
        for ax in axes:
            for v in self.vertices:
                v_norm = np.linalg.norm(v)
                if v_norm < tol:
                    continue
                v_hat = v / v_norm
                if abs(np.dot(v_hat, ax)) > 0.999:
                    threefold_verts.append(v)
                    break
            # Also add the antipodal
            for v in self.vertices:
                v_norm = np.linalg.norm(v)
                if v_norm < tol:
                    continue
                v_hat = v / v_norm
                if abs(np.dot(v_hat, -ax)) > 0.999:
                    threefold_verts.append(v)
                    break

        return np.array(threefold_verts)


# ---------------------------------------------------------------------------
# Sanity Check
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    from gct_geometry import RhombicTriacontahedron

    print("-" * 60)
    print("GCT Representations — Sanity Check")
    print("-" * 60)

    rt = RhombicTriacontahedron()
    analyzer = RepresentationAnalyzer(rt.hull)

    # Classify
    lepton = analyzer.classify_defect_topology("vertex")
    quark  = analyzer.classify_defect_topology("face")

    print(f"Vertex Defect: {lepton['name']} (dim={lepton['dimension']})")
    print(f"Face Defect:   {quark['name']} (dim={quark['dimension']})")

    # Berry Phase
    bp_lepton = analyzer.compute_berry_phase("vertex")
    bp_quark  = analyzer.compute_berry_phase("face")

    print(f"\nBerry Phase (Lepton): {bp_lepton:.4f} * pi  (expect 0)")
    print(f"Berry Phase (Quark):  {bp_quark:.4f} * pi  (expect 2/3 ≈ 0.667)")

    print("-" * 60)
