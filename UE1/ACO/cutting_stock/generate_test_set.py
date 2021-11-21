import random
import pickle

test_ns = [20,200,500]

L = 50

test_set = {}

#objects to cut
for n in test_ns:
	tests = []
	for i in range(50):
		tests.append([L, [random.randint(2, L-int(L/2)) for i in range(n)]])
	test_set[str(n)] = tests


pickle_out = open("csp_testset.pickle","wb")
pickle.dump(test_set, pickle_out)
pickle_out.close()