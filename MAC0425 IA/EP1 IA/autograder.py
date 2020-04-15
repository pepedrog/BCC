import os,sys
from ep1 import *


def part1Test(unigramCost):
	expected = [('',''),
	('twowords','two words'),
    ('assimpleasthat','as simple as that'),
    ('imagineallthepeople','imagine all the people'),
    ('thisisnotmybeautifulhouse', 'this is not my beautiful house')]
	totalTests = 5
	testResults = 0
	print('######################################################')
	print('# Starting tests: (Part01) Segment Words             #')
	print('######################################################')
	try:
		assert type(segmentWords('word', unigramCost)) is str, 'segmentWords returned non string'
		for element in expected:
			if segmentWords(element[0],unigramCost)== element[1]:
				testResults +=1
	except IOError as e:
		print('Error!')
		print('Problems in segmentWords')
		print('################################################')
		print('Python error: {0}'.format(e))
		print('################################################')
	except NotImplementedError:
		print('Error!')
		print('Problems in segmentWords')
		print('Not implemented function')
	except AssertionError as e:
		print('Error!')
		print('Problems in segmentWords')
		print('Returned non string')
		print('################################################')
		print('Python error: {0}'.format(e))
		print('################################################')
	except NameError as e:
		print('Error!')
		print('Problems in segmentWords')
		print('################################################')
		print('Python error: {0}'.format(e))
		print('################################################')
	except Exception as e:
		print('Error!')
		print('Problems in segmentWords')
		print('Unexpected problem')
		print('Check: {0}'.format(e))
		print('################################################')
	else:
		print('#############################################################')
		print('# Congratulations, your code at least run without errors    #')
		print('#############################################################')
	finally:
		print('Results:')
		print('In part01:')
		print('You got {0} out of {1} possible points'.format(testResults, totalTests))
		return testResults

def getRealCosts(corpus='corpus.txt'):
	print('Training language cost functions [corpus: ',  corpus,']...' )
	_realUnigramCost, _realBigramCost = util.makeLanguageModels(corpus)
	_possibleFills = util.makeInverseRemovalDictionary(corpus, 'aeiou')
	print('Done!')
	sys.stdout.flush()
	return _realUnigramCost, _realBigramCost, _possibleFills



def part2Test(bigramCost,possibleFills):
	totalTests = 5
	testResults = 0
	expected = [('',''),
	('zz$z$zz','zz$z$zz'),
	('m p','me up'),
	('wld lk t hv mr lttrs','would like to have more letters'),
	('ngh lrdy','enough already')]
	print('######################################################')
	print('# Starting tests: (Part02) Insert Vowels             #')
	print('######################################################')
	try:
		assert type(insertVowels('m p'.split(), bigramCost, possibleFills)) is str, 'insertVowels returned non string'
		for element in expected:
			if insertVowels(element[0].split(), bigramCost, possibleFills)== element[1]:
				testResults +=1
			else:
				print(insertVowels(element[0].split(), bigramCost, possibleFills), element[1])

	except IOError as e:
		print('Error!')
		print('Problems in insertVowesl')
		print('################################################')
		print('Python error: {0}'.format(e))
		print('################################################')
	except NotImplementedError:
		print('Error!')
		print('Problems in insertVowels')
		print('Not implemented function')
	except AssertionError as e:
		print('Error!')
		print('Problems in insertVowels')
		print('Returned non string')
		print('################################################')
		print('Python error: {0}'.format(e))
		print('################################################')
	except NameError as e:
		print('Error!')
		print('Problems in insertVowels')
		print('################################################')
		print('Python error: {0}'.format(e))
		print('################################################')
	except Exception as e:
		print('Error!')
		print('Problems in insertVowels')
		print('Unexpected problem')
		print('Check: {0}'.format(e))
		print('################################################')
	else:
		print('#############################################################')
		print('# Congratulations, your code at least run without errors    #')
		print('#############################################################')
	finally:
		print('Results:')
		print('In part02:')
		print('You got {0} out of {1} possible points'.format(testResults, totalTests))
		return testResults


def run_tests():
    totalGlobal = 0
    totalTestsGlobal = 10
    unigramCost, bigramCost, possibleFills  =  getRealCosts()
    totalGlobal += part1Test(unigramCost)
    totalGlobal += part2Test(bigramCost,possibleFills)
    print('#############################################################')
    print('# Your final score in this simple tests are:                #')
    print('#############################################################')
    print('   {0} out of {1} possible points: {2:3.1f} grade'.format(totalGlobal,totalTestsGlobal, (totalGlobal/totalTestsGlobal)*10))
    print('#############################################################')
    print('# IMPORTANT: The final tests may check for corner cases     #')
    print('#            that were not tested here. Meaning that this   #')
    print('#            score report is just an example.               #')
    print('#            Your final grade can be much lower than that.  #')
    print('#############################################################')


if __name__ == "__main__":
    FILE_ABSOLUTE_PATH = os.path.abspath(__file__)
    TEST_DIR = os.path.dirname(FILE_ABSOLUTE_PATH)
    run_tests()
