from __future__ import annotations
from typing import Dict, Optional, List
import numpy as np, math

CATEGORIES = ["latency","retrieval","security","wallet","mining","zk","coinjoin","ui"]

def _clip01(x: float) -> float: return max(0.0, min(1.0, float(x)))
def _rng(seed: Optional[int]): return np.random.default_rng(seed) if seed is not None else np.random.default_rng()

def _classical_sampler(signals: Dict[str, float], seed: Optional[int]) -> np.ndarray:
    trend=_clip01(signals.get("trend_strength",0.5)); vol=_clip01(signals.get("volatility",0.5))
    dev=_clip01(signals.get("dev_velocity",0.5)); frus=_clip01(signals.get("user_frustration",0.2))
    cost=_clip01(signals.get("infra_cost",0.4)); sec=_clip01(signals.get("security_findings",0.1))
    alpha = np.array([
        0.6+3.0*frus+0.8*vol, 0.6+2.2*trend+0.4*dev, 0.6+3.2*sec+0.6*vol, 0.6+1.6*frus+0.6*trend,
        0.6+1.2*dev+0.6*vol,  0.6+1.4*dev+0.4*trend, 0.6+0.8*vol+0.6*trend, 0.6+1.0*trend+0.4*cost
    ], dtype=float)
    alpha = np.maximum(alpha, 1e-3)
    return _rng(seed).dirichlet(alpha)

def _pennylane_sampler(signals: Dict[str, float], seed: Optional[int]):
    try:
        import pennylane as qml
    except Exception:
        return None
    a=2*math.pi*_clip01(signals.get('trend_strength',0.5)+0.15*_clip01(signals.get('dev_velocity',0.5)))
    b=2*math.pi*_clip01(0.5*_clip01(signals.get('volatility',0.5))+0.5*_clip01(signals.get('user_frustration',0.2)))
    c=2*math.pi*_clip01(0.6*_clip01(signals.get('security_findings',0.1))+0.4*_clip01(signals.get('infra_cost',0.4)))
    try: dev_pl = qml.device("lightning.qubit", wires=3, shots=4096, seed=seed)
    except Exception: dev_pl = qml.device("default.qubit", wires=3, shots=4096, seed=seed)
    @qml.qnode(dev_pl)
    def circ(a,b,c):
        qml.RY(a,0); qml.RZ(a/2,0); qml.RY(b,1); qml.RZ(b/2,1); qml.RY(c,2); qml.RZ(c/2,2)
        qml.Hadamard(0); qml.PauliX(1); qml.SWAP([0,1]); qml.CNOT([1,2]); qml.Hadamard(0)
        return qml.sample(wires=[0,1,2])
    try: samples = circ(a,b,c)
    except Exception: return None
    counts = np.zeros(8, dtype=float)
    for q0,q1,q2 in samples:
        counts[(int(q0)<<2)|(int(q1)<<1)|int(q2)] += 1.0
    return (counts+1e-9)/(counts.sum()+8e-9)

def _qiskit_sampler(signals: Dict[str, float], seed: Optional[int]):
    try:
        from qiskit import QuantumCircuit, Aer, execute
        from qiskit.utils import algorithm_globals
    except Exception:
        return None
    algorithm_globals.random_seed = seed if seed is not None else 1234
    a=2*math.pi*_clip01(signals.get('trend_strength',0.5)+0.15*_clip01(signals.get('dev_velocity',0.5)))
    b=2*math.pi*_clip01(0.5*_clip01(signals.get('volatility',0.5))+0.5*_clip01(signals.get('user_frustration',0.2)))
    c=2*math.pi*_clip01(0.6*_clip01(signals.get('security_findings',0.1))+0.4*_clip01(signals.get('infra_cost',0.4)))
    qc=QuantumCircuit(3,3)
    for i,x in enumerate([a,b,c]): qc.ry(x,i); qc.rz(x/2,i)
    qc.h(0); qc.x(1); qc.swap(0,1); qc.cx(1,2); qc.h(0); qc.measure([0,1,2],[0,1,2])
    try: backend = Aer.get_backend('qasm_simulator')
    except Exception: return None
    result = execute(qc, backend, shots=4096, seed_simulator=seed, seed_transpiler=seed).result()
    counts = result.get_counts(); total = sum(counts.values())
    probs = np.zeros(8, dtype=float)
    for bits,c in counts.items(): probs[int(bits,2)] = c/total
    return (probs+1e-9)/(probs.sum()+8e-9)

def get_available_modes()->List[str]:
    m=["classical"]
    try: import pennylane; m.append("pennylane")
    except Exception: pass
    try: import qiskit; m.append("qiskit")
    except Exception: pass
    return m

def sample8(signals: Dict[str,float], mode:str="auto", seed: Optional[int]=None):
    mode=(mode or "auto").lower().strip()
    if mode=="auto":
        p=_pennylane_sampler(signals,seed)
        return p if p is not None else _classical_sampler(signals,seed)
    if mode=="pennylane":
        p=_pennylane_sampler(signals,seed); 
        if p is None: raise RuntimeError("PennyLane not available")
        return p
    if mode=="qiskit":
        p=_qiskit_sampler(signals,seed); 
        if p is None: raise RuntimeError("Qiskit not available")
        return p
    return _classical_sampler(signals,seed)
