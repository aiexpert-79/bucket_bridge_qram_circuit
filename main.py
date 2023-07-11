import cirq
from qramcircuits.toffoli_decomposition import ToffoliDecompType, ToffoliDecomposition
from mathematics.draper0406142 import CarryLookaheadAdder
import qramcircuits.bucket_brigade as bb
import qramcircuits.small_depth_large_width as sdlw
import qramcircuits.large_depth_small_width as ldsw
from qramcircuits.mpmct_decomposition import *
import optimizers as qopt
import utils.counting_utils as cu
import os
import math

def main():
    print("Hello QRAM circuits!")

    # Create the qubis of the circuits
    file_size = os.path.getsize(r"E:\task\a.txt")
    file_bit_size = file_size * 8 
    nr_qubits = math.ceil(math.log2(file_bit_size))
    print(nr_qubits)
    
    qubits = []

    for i in range(nr_qubits):
        qubits.append(cirq.NamedQubit("a" + str(i)))

    # Create the search
    search = [0, 1, 2, 3]
    search = list(range(0, 7))

    """
       # Bucket brigade
    """
    print("*** Bucket Brigade:")

    decomp_scenario = bb.BucketBrigadeDecompType(
        [
            ToffoliDecompType.ZERO_ANCILLA_TDEPTH_4_COMPUTE,  # fan_in_decomp
            ToffoliDecompType.ZERO_ANCILLA_TDEPTH_4,  # mem_decomp
            ToffoliDecompType.ZERO_ANCILLA_TDEPTH_0_UNCOMPUTE,  # fan_out_decomp
        ],
        True,
    )

    no_decomp = bb.BucketBrigadeDecompType(
        [
            ToffoliDecompType.NO_DECOMP,  # fan_in_decomp
            ToffoliDecompType.NO_DECOMP,  # mem_decomp
            ToffoliDecompType.NO_DECOMP,  # fan_out_decomp
        ],
        True,
    )

    olivia_decomposition = bb.BucketBrigadeDecompType(
        [
            ToffoliDecompType.FOUR_ANCILLA_TDEPTH_1_A,  # fan_in_decomp
            ToffoliDecompType.FOUR_ANCILLA_TDEPTH_1_A,  # mem_decomp
            ToffoliDecompType.FOUR_ANCILLA_TDEPTH_1_A,  # fan_out_decomp
        ],
        False,
    )

    bbcircuit = bb.BucketBrigade(qubits, decomp_scenario=decomp_scenario)
    
    print(
        bbcircuit.circuit.to_text_diagram(
            use_unicode_characters=False, qubit_order=bbcircuit.qubit_order
        )
    )

    # Verification
    print("Verify N_q:      {}\n".format(bbcircuit.verify_number_qubits()))
    print("Verify D:        {}\n".format(bbcircuit.verify_depth(
        Alexandru_scenario=decomp_scenario.parallel_toffolis)
        )
    )
    print("Verify T_c:      {}\n".format(bbcircuit.verify_T_count()))
    print("Verify T_d:      {}\n".format(bbcircuit.verify_T_depth(
                Alexandru_scenario=decomp_scenario.parallel_toffolis
            )
        )
    )
    print(
        "Verify H_c:      {}\n".format(
            bbcircuit.verify_hadamard_count(
                Alexandru_scenario=decomp_scenario.parallel_toffolis
            )
        )
    )
    print(
        "Verify CNOT_c:   {}\n".format(
            bbcircuit.verify_cnot_count(
                Alexandru_scenario=olivia_decomposition.parallel_toffolis
            )
        )
    )

    qopt.CommuteTGatesToStart().optimize_circuit(bbcircuit.circuit)

    # print(bbcircuit.circuit)

    qopt.SearchCNOTPattern().optimize_circuit(bbcircuit.circuit)

    qopt.CancelNghCNOTs().apply_until_nothing_changes(bbcircuit.circuit,
                                                      cu.count_cnot_of_circuit)
    print("*** Large Depth Small Width:")
    # """
    # be sure while testing that the number of search values are a power of 2
    # and that the binary decomposition of each search value is less or equal to the number of qubits' address
    # like if we have 4 qubits then the search values should range between 0 and 15
    # """

    # ldsmcircuit = ldsw.LargeDepthSmallWidth(qubits,
    #                                         search,
    #                                         decomp_type = MPMCTDecompType.ALLOW_DECOMP)
    # print((ldsmcircuit.circuit))
    # print("Verify N_q:      {}\n".format(ldsmcircuit.verify_number_qubits()))
    # print("Verify D:        {}\n".format(ldsmcircuit.verify_depth()))
    # print("Verify T_c:      {}\n".format(ldsmcircuit.verify_T_count()))
    # print("Verify T_d:      {}\n".format(ldsmcircuit.verify_T_depth()))
    # print("Verify H_c:      {}\n".format(ldsmcircuit.verify_hadamard_count()))
    # print("Verify CNOT_c:   {}\n".format(ldsmcircuit.verify_cnot_count()))
    # qopt.CommuteTGatesToStart().optimize_circuit(ldsmcircuit.circuit)

    print("*** Small Depth Large Width:")
    # #be sure while testing that the number of search values are a power of 2
    # #and that the binary decomposition of each search value is less or equal to the number of qubits' address
    # # like if we have 4 qubits then the search values should range between 0 and 15
    # sdlwcircuit = sdlw.SmallDepthLargeWidth(qubits,
    #                                         search,
    #                                         decomp_type = MPMCTDecompType.ALLOW_DECOMP)
    # print(sdlwcircuit.circuit)
    # print("Verify N_q:      {}\n".format(sdlwcircuit.verify_number_qubits()))
    # print("Verify D:        {}\n".format(sdlwcircuit.verify_depth()))  #still working on the depth
    # print("Verify T_d:      {}\n".format(sdlwcircuit.verify_T_depth()))
    # print("Verify T_c:      {}\n".format(sdlwcircuit.verify_T_count()))
    # print("Verify H_c:      {}\n".format(sdlwcircuit.verify_hadamard_count()))
    # print("Verify CNOT_c:   {}\n".format(sdlwcircuit.verify_cnot_count()))

    """
        CLA example
    """
    # Size of the operand; At this stage always gives the even number >= to the wanted size
    # n = 3
    # A = [cirq.NamedQubit("A" + str(i)) for i in range(n)]

    # # Second operand
    # B = [cirq.NamedQubit("B" + str(i)) for i in range(n)]

    # # CLA class with the default decomposition strategy (NO_DECOMP)
    # decompositon_strategy = [
    #     (ToffoliDecompType.NO_DECOMP, ToffoliDecompType.NO_DECOMP)
    # ] * 2
    # cl = CarryLookaheadAdder(A, B, decompositon_strategy=decompositon_strategy)
    # # Printing the CLA circuit
    # print(cl.circuit)

    results = []
    for n in range(2, 8, 2):
        # First operand
        A = [cirq.NamedQubit("A" + str(i)) for i in range(n)]

        # Second operand
        B = [cirq.NamedQubit("B" + str(i)) for i in range(n)]

        # CLA class with the default decomposition strategy (NO_DECOMP)
        decompositon_strategy = [
            (ToffoliDecompType.NO_DECOMP, ToffoliDecompType.NO_DECOMP)
        ] * 2
        cl = CarryLookaheadAdder(A, B, decompositon_strategy=decompositon_strategy)
        # Printing the CLA circuit
        results.append(len(cl.circuit))
    print(results)


if __name__ == "__main__":
    main()
