import numpy as np
import json
import os
from pathlib import Path
import sys
from gct_utils import C

# Add src to path for gct_utils
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
try:
    from gct_utils import C, get_output_path
except ImportError:
    # Fallback if utils are not on the import path
    class C:
        PHI = float(C.PHI)
    def get_output_path(name):
        return name

def ra_dec_to_cartesian(ra_deg, dec_deg):
    ra_rad = np.radians(ra_deg)
    dec_rad = np.radians(dec_deg)
    x = np.cos(dec_rad) * np.cos(ra_rad)
    y = np.cos(dec_rad) * np.sin(ra_rad)
    z = np.sin(dec_rad)
    return np.array([x, y, z])

def cartesian_to_ra_dec(vec):
    vec = vec / np.linalg.norm(vec)
    dec = np.degrees(np.arcsin(vec[2]))
    ra = np.degrees(np.arctan2(vec[1], vec[0]))
    if ra < 0:
        ra += 360
    return ra, dec

def get_icosahedron_vertices():
    phi = C.PHI
    verts = []
    # (0, +-1, +-phi)
    for s1 in [-1, 1]:
        for s2 in [-1, 1]:
            verts.append([0, s1, s2 * phi])
    # (+-1, +-phi, 0)
    for s1 in [-1, 1]:
        for s2 in [-1, 1]:
            verts.append([s1, s2 * phi, 0])
    # (+-phi, 0, +-1)
    for s1 in [-1, 1]:
        for s2 in [-1, 1]:
            verts.append([s1 * phi, 0, s2])
    
    verts = np.array(verts)
    norms = np.linalg.norm(verts, axis=1)
    return verts / norms[:, np.newaxis]

def rotation_matrix_to_align(v_from, v_to):
    """Returns matrix R such that R @ v_from = v_to."""
    v_from = v_from / np.linalg.norm(v_from)
    v_to = v_to / np.linalg.norm(v_to)
    v = np.cross(v_from, v_to)
    c = np.dot(v_from, v_to)
    s = np.linalg.norm(v)
    
    if s < 1e-12:
        if c > 0:
            return np.eye(3)
        else:
            # Opposite vectors: 180 deg rotation
            return -np.eye(3) # Not unique, but works for alignment
            
    kmat = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
    rotation_matrix = np.eye(3) + kmat + kmat.dot(kmat) * ((1 - c) / (s**2))
    return rotation_matrix

def rotation_around_axis(axis, theta):
    axis = axis / np.linalg.norm(axis)
    a = np.cos(theta / 2.0)
    b, c, d = -axis * np.sin(theta / 2.0)
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return np.array([[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
                     [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
                     [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]])

def solve_alignment():
    # Constants
    CMB_DIPOLE_RA = 167.9
    CMB_DIPOLE_DEC = -6.9
    TA_HOTSPOT_RA = 146.7
    TA_HOTSPOT_DEC = 43.2
    HOTSPOT_RADIUS = 20.0
    
    v_cmb = ra_dec_to_cartesian(CMB_DIPOLE_RA, CMB_DIPOLE_DEC)
    v_ta = ra_dec_to_cartesian(TA_HOTSPOT_RA, TA_HOTSPOT_DEC)
    
    verts = get_icosahedron_vertices()
    
    # Align one vertex to CMB dipole
    # We'll use the first vertex [0, 1, phi] normalized
    v0 = verts[0]
    R_align = rotation_matrix_to_align(v0, v_cmb)
    verts_aligned = (R_align @ verts.T).T
    
    min_sep = 180.0
    best_psi = 0
    best_ra, best_dec = 0, 0
    
    # Scan azimuth psi
    for psi in np.linspace(0, np.radians(72), 360):
        R_rot = rotation_around_axis(v_cmb, psi)
        verts_final = (R_rot @ verts_aligned.T).T
        
        # Check all vertices except the one at CMB (index 0)
        for i in range(1, 12):
            v = verts_final[i]
            # Use dot product for angular separation
            cos_sep = np.clip(np.dot(v, v_ta), -1.0, 1.0)
            sep = np.degrees(np.arccos(cos_sep))
            
            if sep < min_sep:
                min_sep = sep
                best_psi = psi
                best_ra, best_dec = cartesian_to_ra_dec(v)
                
    verdict = "PASS" if min_sep < HOTSPOT_RADIUS else "FAIL"
    
    results = {
        "protocol": "protocol_ta_hotspot",
        "description": "Alignment of icosahedral vacuum against TA UHECR Hotspot (CMB Rest Frame)",
        "cmb_dipole": {"ra": CMB_DIPOLE_RA, "dec": CMB_DIPOLE_DEC},
        "ta_hotspot": {"ra": TA_HOTSPOT_RA, "dec": TA_HOTSPOT_DEC},
        "predicted_axis": {"ra": best_ra, "dec": best_dec},
        "min_separation_deg": float(min_sep),
        "hotspot_radius_deg": float(HOTSPOT_RADIUS),
        "azimuth_offset_deg": float(np.degrees(best_psi)),
        "verdict": verdict,
        "pass": bool(min_sep < HOTSPOT_RADIUS)
    }
    
    print(f"TA Hotspot Audit Complete.")
    print(f"Min Separation: {min_sep:.2f} degrees")
    print(f"Verdict: {verdict}")
    
    output_path = get_output_path("protocol_ta_hotspot_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)
        
if __name__ == "__main__":
    solve_alignment()
