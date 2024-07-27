import numpy as np

def rbc_model(alpha, beta, delta, A1, A2, K1):
    # Utility function parameters
    sigma = 2
    
    # Production function
    Y1 = A1 * K1
    K2 = (1 - delta) * K1 + A1 * K1
    
    # Solve for consumption and investment
    C1 = (beta * A2) ** (1 / sigma) * A2 * Y1 / (1 + (beta * A2) ** (1 / sigma))
    C2 = A2 * Y1 / (1 + (beta * A2) ** (1 / sigma))
    I1 = Y1 - C1
    Y2 = A2 * K2
    
    return C1, C2, I1, Y1, Y2

def new_keynesian_model(alpha, beta, delta, A1, A2, K1, phi):
    # Utility function parameters
    sigma = 2
    # Money supply
    M1 = 100
    M2 = 110
    
    # Production function
    Y1 = A1 * K1
    K2 = (1 - delta) * K1 + A1 * K1
    
    # Sticky prices (nominal rigidity)
    P1 = 1
    P2 = P1 * (1 + phi * (M2 - M1) / M1)
    
    # Solve for consumption and investment
    C1 = (beta * A2) ** (1 / sigma) * A2 * Y1 / (1 + (beta * A2) ** (1 / sigma))
    C2 = A2 * Y1 / (1 + (beta * A2) ** (1 / sigma))
    I1 = Y1 - C1
    Y2 = A2 * K2
    
    return C1, C2, I1, Y1, Y2, P1, P2

def cia_model(alpha, beta, delta, A1, A2, K1, M1, M2):
    # Utility function parameters
    sigma = 2
    
    # Production function
    Y1 = A1 * K1
    K2 = (1 - delta) * K1 + A1 * K1
    
    # Cash-in-advance constraint
    V1 = M1 / (A1 * K1)
    V2 = M2 / (A2 * K2)
    
    # Solve for consumption and investment
    C1 = (beta * A2) ** (1 / sigma) * A2 * Y1 / (1 + (beta * A2) ** (1 / sigma))
    C2 = A2 * Y1 / (1 + (beta * A2) ** (1 / sigma))
    I1 = Y1 - C1
    Y2 = A2 * K2
    
    return C1, C2, I1, Y1, Y2, V1, V2

# Example parameters
alpha = 0.36
beta = 0.96
delta = 0.1
A1 = 1.0
A2 = 1.1
K1 = 10.0
phi = 0.5
M1 = 100
M2 = 110

# Real Business Cycle (RBC) Model
C1_rbc, C2_rbc, I1_rbc, Y1_rbc, Y2_rbc = rbc_model(alpha, beta, delta, A1, A2, K1)
print("Real Business Cycle (RBC) Model:")
print(f'C1: {C1_rbc}, C2: {C2_rbc}, I1: {I1_rbc}, Y1: {Y1_rbc}, Y2: {Y2_rbc}')

# New Keynesian Model
C1_nk, C2_nk, I1_nk, Y1_nk, Y2_nk, P1_nk, P2_nk = new_keynesian_model(alpha, beta, delta, A1, A2, K1, phi)
print("\nNew Keynesian Model:")
print(f'C1: {C1_nk}, C2: {C2_nk}, I1: {I1_nk}, Y1: {Y1_nk}, Y2: {Y2_nk}, P1: {P1_nk}, P2: {P2_nk}')

# Cash-in-Advance (CIA) Model
C1_cia, C2_cia, I1_cia, Y1_cia, Y2_cia, V1_cia, V2_cia = cia_model(alpha, beta, delta, A1, A2, K1, M1, M2)
print("\nCash-in-Advance (CIA) Model:")
print(f'C1: {C1_cia}, C2: {C2_cia}, I1: {I1_cia}, Y1: {Y1_cia}, Y2: {Y2_cia}, V1: {V1_cia}, V2: {V2_cia}')
