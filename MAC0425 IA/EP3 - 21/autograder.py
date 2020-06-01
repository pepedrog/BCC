import os
import sys
import random
import math
import signal
import time
import pylint.lint
try:
    from ep3 import *
except Exception as e:
    if os.path.exists("final_result.txt"):
        file_flag = "a"
    else:
        file_flag = "w"

    if os.path.exists("../results.csv"):
        csv_flag = "a"
    else:
        csv_flag = "w"

    file_results = open("final_result.txt", file_flag)
    file_results.write("******************************\n")
    file_results.write("Your code does not even import!\n")
    file_results.write("------------------------------\n")
    file_results.write("Unable to perform any check or test\n")
    file_results.write("Grades are:\nTest01-01: 0.0\nTest01-02: 0.0\n")
    file_results.write("Test02: 0.0\nTest03: 0.0\n")
    file_results.close()
    results_csv = open("../results.csv", csv_flag)
    results_csv.write("-1000.0, 0.0, 0.0, 0.0, 0.0\n")
    results_csv.close()
    sys.exit(1)


TOLERANCE = 0.0001
MAX_TESTS = 50


class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass

    def __init__(self, sec):
        self.sec = sec

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.alarm(self.sec)

    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm

    def raise_timeout(self, *args):
        raise Timeout.Timeout()


def run_tests():
    if os.path.exists("final_result.txt"):
        file_flag = "a"
    else:
        file_flag = "w"
    file_results = open("final_result.txt", file_flag)
    final_grades = [0.0,0.0,0.0,0.0,0.0,0.0,0.0]  # Grade list (code, p01_01, p01_02, p02, p03)
    lint_result = pylint.lint.Run(['ep3.py'], do_exit=False)
    for k in lint_result.linter.stats["by_module"]:
        mod_name = k
    msg_types = lint_result.linter.stats["by_module"][mod_name]
    msg_names = lint_result.linter.stats['by_msg']
    if 'global_note' in lint_result.linter.stats:
        lint_score = lint_result.linter.stats['global_note']
    else:
        lint_score = -1000.0
    file_results.write("******************************\n")
    file_results.write("Code quality:\n")
    file_results.write("------------------------------\n")
    file_results.write("Code grade: {0:.2f}/10.0".format(lint_score))
    if lint_score < 0:
        file_results.write("\t(Code has serious problems)\n")
    elif lint_score < 5.0:
        file_results.write("\t(Code need some adjustments)\n")
    elif lint_score < 7.0:
        file_results.write("\t(Code with reasonably quality)\n")
    else:
        file_results.write("\t(Great code quality)\n")
    file_results.write("------------------------------\n")
    file_results.write("Standards deviation:\n")
    for k1, v1 in msg_types.items():
        file_results.write("{0}:\t{1}\n".format(k1, v1))
    file_results.write("------------------------------\n")
    file_results.write("Deviation description:\n")
    for k2, v2 in msg_names.items():
        file_results.write("{0}:\t{1}\n".format(k2, v2))
    file_results.write("******************************\n")
    file_results.write("Tests:\n")
    final_grades[0]=lint_score

    global_results = 0  # Student's result in all tests for all parts
    total_tests_global = 0  # Number of tests performed in all parts
    total_tests = 0  # Number of tests in a specific part
    test_results = 0  # Student's result in that specific
    aux_counter = 0  # Auxiliar counter to limit number of tests
    part_tests = 0  # Keep total tests in each part for weighted score
    part_correct = 0  # Keep correct in each part for weighted score

    try:
        file_results.write("------------------------------\n")
        file_results.write("Parte01-01 Modeling MDPs:\n")
        smallMDP = BlackjackMDP(valores_cartas=[1, 5], multiplicidade=2,
                                       limiar=15, custo_espiada=1)
        preEmptyState = (11, None, (1,0))
        # Make sure the succAndProbReward function is implemented correctly.
        tests = [
            ([((12, None, None), 1, 12)], smallMDP, preEmptyState, 'Pegar'),
            ([((5, None, (2, 1)), 1, 0)], smallMDP, (0, 1, (2, 2)), 'Pegar')
        ]
        for gold, mdp, state, action in tests:
            total_tests_global += 1
            total_tests += 1
            with Timeout(10):
                if  gold==mdp.succAndProbReward(state, action):
                    test_results += 1
        file_results.write("Modeling MDPs:\t{0}/{1} correct\n".format(test_results, total_tests))
        global_results += test_results
        part_correct += test_results
        part_tests += total_tests
        test_results = 0
        total_tests = 0
        if part_tests > 0:
            final_grades[1]=(10.0*part_correct)/part_tests
        part_correct = 0
        part_tests = 0
        # End of Part01
    except IOError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except NotImplementedError:
        file_results.write("NotImplemented\n")
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except AssertionError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except NameError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except Timeout.Timeout:
        file_results.write("Test did not conclude in time\n")
        file_results.write("Receiving proportional grade in the test\n")
        final_grades[1]=(10.0*test_results)/2.0
    except Exception as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    else:
        file_results.write("Test concluded without errors\n")
        
    finally:
        file_results.write("Grade in the Test01: {0:.1f}/10.0\n".format(final_grades[1]))

    try:
        test_results = 0
        total_tests = 0
        file_results.write("------------------------------\n")
        file_results.write("Part02-01 ValueIteration::\n")
        alg = ValueIteration()
        with Timeout(10):
            alg.solve(smallMDP)
        total_tests_global += 1
        total_tests += 1
        samePolicy = True
        for _, val in alg.pi.items():
            if val=="Espiar":
                samePolicy = False
        if samePolicy:
            test_results +=1
        file_results.write("ValueIteration:\t{0}/{1} correct\n".format(test_results, total_tests))
        global_results += test_results
        part_correct += test_results
        part_tests += total_tests
        test_results = 0
        total_tests = 0

        if part_tests > 0:
            final_grades[2] = (10.0*part_correct)/part_tests
        part_correct = 0
        part_tests = 0
        # End of Part02-01
    except IOError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except NotImplementedError:
        file_results.write("NotImplemented\n")
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except AssertionError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except NameError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except Timeout.Timeout:
        file_results.write("Test did not conclude in time\n")
        file_results.write("Receiving proportional grade in the test\n")
        final_grades[2] = (10.0*test_results)
    except Exception as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    else:
        file_results.write("Test concluded without errors\n")
        #file_results.write("Grade in the test: {0:.1f}/10.0\n".format(final_grades[0]))
    finally:
        file_results.write("Grade in the Test02-01: {0:.1f}/10.0\n".format(final_grades[2]))


    try:
        test_results = 0
        total_tests = 0
        file_results.write("------------------------------\n")
        file_results.write("Part02-02 Peeking MDP:\n")

        
        mdpP = geraMDPxereta()
        vi = ValueIteration()
        with Timeout(10):
            vi.solve(mdpP)
        total_tests_global += 1
        total_tests += 1
        f = len([a for a in vi.pi.values() if a == 'Espiar']) / float(len(vi.pi.values()))
        if f >= 0.1:
            test_results +=1
        file_results.write("Peeking MDP:\t{0}/{1} correct\n".format(test_results, total_tests))
        global_results += test_results
        part_correct += test_results
        part_tests += total_tests
        test_results = 0
        total_tests = 0

        if part_tests > 0:
            final_grades[2] = (10.0*part_correct)/part_tests
        part_correct = 0
        part_tests = 0
        # End of Part02-02
    except IOError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except NotImplementedError:
        file_results.write("NotImplemented\n")
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except AssertionError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except NameError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except Timeout.Timeout:
        file_results.write("Test did not conclude in time\n")
        file_results.write("Receiving proportional grade in the test\n")
        final_grades[2] = (10.0*test_results)
    except Exception as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    else:
        file_results.write("Test concluded without errors\n")
        #file_results.write("Grade in the test: {0:.1f}/10.0\n".format(final_grades[0]))
    finally:
        file_results.write("Grade in the Test02-02: {0:.1f}/10.0\n".format(final_grades[2]))


    try:
        test_results = 0
        total_tests = 0
        file_results.write("------------------------------\n")
        file_results.write("Part03-01 QLearningAlgorithm:\n")
        #-------------------------------------------------
        total_tests_global += 4
        total_tests += 4
        lineMDP = util.NumberLineMDP()
        lineMDP.computeStates()
        with Timeout(10):
            rl = QLearningAlgorithm(lineMDP.actions, lineMDP.discount(),identityFeatureExtractor,0)
        rl.numIters = 1
        with Timeout(10):
            rl.incorporateFeedback(0, 1, 0, 1)
            if rl.getQ(0, -1)== 0:
                test_results +=1
            if rl.getQ(0, 1) == 0:
                test_results +=1
        with Timeout(10):
            rl.incorporateFeedback(2, -1, 1, 1)
            if rl.getQ(2, -1) == 1:
                test_results += 1
            if rl.getQ(2, 1) == 0:
                test_results += 1
        #-------------------------------------------------
        file_results.write("QLearningAlgorithm:\t{0}/{1} correct\n".format(test_results, total_tests))
        global_results += test_results
        part_correct += test_results
        part_tests += total_tests
        test_results = 0
        total_tests = 0

        if part_tests > 0:
            final_grades[3] = (10.0*part_correct)/part_tests
        part_correct = 0
        part_tests = 0
        # End of Part03-01
    except IOError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except NotImplementedError:
        file_results.write("NotImplemented\n")
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except AssertionError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except NameError as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    except Timeout.Timeout:
        file_results.write("Test did not conclude in time\n")
        file_results.write("Receiving proportional grade in the test\n")
        final_grades[3] = (10.0*test_results)/4.0
    except Exception as e:
        file_results.write("Python error: {0}\n".format(e))
        file_results.write("Test did not conclude\n")
        file_results.write("Receiving grade 0.0 in the test\n")
    else:
        file_results.write("Test concluded without errors\n")
        #file_results.write("Grade in the test: {0:.1f}/10.0\n".format(final_grades[0]))
    finally:
        file_results.write("Grade in the Test03-01: {0:.1f}/10.0\n".format(final_grades[3]))

    # try:
    #     test_results = 0
    #     total_tests = 0
    #     file_results.write("------------------------------\n")
    #     file_results.write("Part03-02 BlackjackFeatureExtractor:\n")
    #     #-------------------------------------------------------------------
    #     total_tests_global += 2
    #     total_tests += 2
    #     mdp.computeStates()
    #     rl = QLearningAlgorithm(mdp.actions, mdp.discount(),blackjackFeatureExtractor,0)
    #     rl.numIters = 1
    #     with Timeout(10):
    #         rl.incorporateFeedback((7, None, (0, 1)), 'Quit', 7, (7, None, None))
    #         if rl.getQ((7, None, (0, 1)), 'Quit') == 28:
    #             test_results += 1
    #         else:
    #             print(rl.getQ((7, None, (0, 1)), 'Quit'))
    #         if rl.getQ((2, None, (0, 2)), 'Pegar') == 0:
    #             test_results += 1

    #     file_results.write("BlackjackFeatureExtractor:\t{0}/{1} correct\n".format(test_results, total_tests))
    #     global_results += test_results
    #     part_correct += test_results
    #     part_tests += total_tests
    #     test_results = 0
    #     total_tests = 0

    #     if part_tests > 0:
    #         final_grades[4] = (10.0*part_correct)/part_tests
    #     part_correct = 0
    #     part_tests = 0
    #     # End of Part01-01
    # except IOError as e:
    #     file_results.write("Python error: {0}\n".format(e))
    #     file_results.write("Test did not conclude\n")
    #     file_results.write("Receiving grade 0.0 in the test\n")
    # except NotImplementedError:
    #     file_results.write("NotImplemented\n")
    #     file_results.write("Test did not conclude\n")
    #     file_results.write("Receiving grade 0.0 in the test\n")
    # except AssertionError as e:
    #     file_results.write("Python error: {0}\n".format(e))
    #     file_results.write("Test did not conclude\n")
    #     file_results.write("Receiving grade 0.0 in the test\n")
    # except NameError as e:
    #     file_results.write("Python error: {0}\n".format(e))
    #     file_results.write("Test did not conclude\n")
    #     file_results.write("Receiving grade 0.0 in the test\n")
    # except Timeout.Timeout:
    #     file_results.write("Test did not conclude in time\n")
    #     file_results.write("Receiving proportional grade in the test\n")
    #     final_grades[4] = (10.0*test_results)/2.0
    # except Exception as e:
    #     file_results.write("Python error: {0}\n".format(e))
    #     file_results.write("Test did not conclude\n")
    #     file_results.write("Receiving grade 0.0 in the test\n")
    # else:
    #     file_results.write("Test concluded without errors\n")
    #     #file_results.write("Grade in the test: {0:.1f}/10.0\n".format(final_grades[0]))
    # finally:
    #     file_results.write("Grade in the Test03-02: {0:.1f}/10.0\n".format(final_grades[4]))
    
    # Concluding and updating csv with grades
    if os.path.exists("../results.csv"):
        csv_flag = "a"
    else:
        csv_flag = "w"
    #pdb.set_trace()

    results_csv = open("../results.csv", csv_flag)
    if len(final_grades) == 5:
        for grade in final_grades:
            results_csv.write("{0},".format(grade))
        results_csv.write("\n")
    else:
        for i in range(len(final_grades)):
            results_csv.write("{0},".format(final_grades[i]))
        for _ in range(len(final_grades), 5):
            results_csv.write("-1000,")
        results_csv.write("\n")
    results_csv.close()


if __name__ == "__main__":
    FILE_ABSOLUTE_PATH = os.path.abspath(__file__)
    TEST_DIR = os.path.dirname(FILE_ABSOLUTE_PATH)

    run_tests()
