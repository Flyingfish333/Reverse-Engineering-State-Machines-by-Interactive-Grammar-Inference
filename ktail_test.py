from Acceptor import *
import random
import os

def generate_candidate(s):
    candidate = []

    for x in range(len(s)):
        for i in range(len(s) - x):
            if x == 0:
                candidate.append(s[i:i + x + 1])
            elif x < 2:
                for j in range(len(s) - x - i):
                    candidate.append(s[i] + s[j + x + i])
            else:
                for j in range(len(s) - x - i):
                    candidate.append(s[i:i+x] + s[j + x + i])

    return candidate

def random_choice_candidate(candidate, n=8):
    result = []

    for _ in range(n):
        idx = random.randint(0, len(candidate)-1)
        result.append(candidate[idx])
    
    return result

def run_ktail(apta: Acceptor, k):
    ktail = apta.find_ktail(k)
    apta.ktail = ktail
    pair, pair_idx = apta.equal_pair()
    while len(pair) > 0:
        merged_state_tail_idx, merging_state_tail_idx, edge_tail = pair_idx[0]
        apta.merge(merged_state_tail_idx, merging_state_tail_idx, edge_tail)
        ktail = apta.find_ktail(k)
        apta.ktail = ktail
        pair, pair_idx = apta.equal_pair()

def test_5_state(test_n):
    if os.path.exists('test_file/five_state'):
        os.system('rm -rf test_file/five_state')
    
    os.system('mkdir test_file/five_state')
    for i in range(1, test_n+1):
        test_folder = 'test_file/five_state/set%d/' % i
        os.system('mkdir %s' % test_folder)
        s = 'abcde'
        candidate = generate_candidate(s)
        candidate = random_choice_candidate(candidate)

        apta_k1 = Acceptor(1)
        apta_k2 = Acceptor(1)
        apta_k3 = Acceptor(1)
        
        apta_k1.build_tree(candidate)
        apta_k2.build_tree(candidate)
        apta_k3.build_tree(candidate)

        apta_k2.draw_tree(None, None, test_folder+'state_5_original.jpg')

        run_ktail(apta_k1, 1)
        run_ktail(apta_k2, 2)
        run_ktail(apta_k3, 3)

        apta_k1.draw_tree(None, None, test_folder+'state_5_k1.jpg')
        apta_k2.draw_tree(None, None, test_folder+'state_5_k2.jpg')
        apta_k3.draw_tree(None, None, test_folder+'state_5_k3.jpg')

def test_10_state(test_n):
    if os.path.exists('test_file/ten_state'):
        os.system('rm -rf test_file/ten_state')
        
    os.system('mkdir test_file/ten_state')
    for i in range(1, test_n+1):
        test_folder = 'test_file/ten_state/set%d/' % i
        os.system('mkdir %s' % test_folder)

        s = ''
        for i in range(0, 10):
            s += chr(ord('a')+i)

        candidate = generate_candidate(s)
        candidate = random_choice_candidate(candidate)
        # with open('states_10.txt', 'w') as f:
        #     for s in candidate:
        #         f.write(s+'\n')

        # apta_k2 = Acceptor(1)
        apta_k3 = Acceptor(1)
        apta_k4 = Acceptor(1)
        apta_k5 = Acceptor(1)
        
        # apta_k2.build_tree(candidate)
        apta_k3.build_tree(candidate)
        apta_k4.build_tree(candidate)
        apta_k5.build_tree(candidate)

        apta_k3.draw_tree(None, None, test_folder+'state_10_original.jpg')

        # run_ktail(apta_k2, 2)
        run_ktail(apta_k3, 3)
        run_ktail(apta_k4, 4)
        run_ktail(apta_k5, 5)

        # apta_k2.draw_tree(None, None, os.getcwd()+'/test_file/state_10_k2.jpg')
        apta_k3.draw_tree(None, None, test_folder+'state_10_k3.jpg')
        apta_k4.draw_tree(None, None, test_folder+'state_10_k4.jpg')
        apta_k5.draw_tree(None, None, test_folder+'state_10_k5.jpg')

def test_15_state(test_n):
    if os.path.exists('test_file/fifteen_state'):
        os.system('rm -rf test_file/fifteen_state')
        
    os.system('mkdir test_file/fifteen_state')
    for i in range(1, test_n+1):
        test_folder = 'test_file/fifteen_state/set%d/' % i
        os.system('mkdir %s' % test_folder)

        s = ''
        for i in range(0, 15):
            s += chr(ord('a')+i)

        candidate = generate_candidate(s)
        candidate = random_choice_candidate(candidate)

        # apta_k2 = Acceptor(1)
        apta_k3 = Acceptor(1)
        apta_k4 = Acceptor(1)
        apta_k5 = Acceptor(1)
        
        # apta_k2.build_tree(candidate)
        apta_k3.build_tree(candidate)
        apta_k4.build_tree(candidate)
        apta_k5.build_tree(candidate)

        apta_k3.draw_tree(None, None, test_folder+'state_15_original.jpg')

        # run_ktail(apta_k2, 2)
        run_ktail(apta_k3, 3)
        run_ktail(apta_k4, 4)
        run_ktail(apta_k5, 5)

        # apta_k2.draw_tree(None, None, os.getcwd()+'/test_file/state_10_k2.jpg')
        # apta_k3.draw_tree(None, None, test_folder+'state_15_k3.jpg')
        apta_k4.draw_tree(None, None, test_folder+'state_15_k4.jpg')
        apta_k5.draw_tree(None, None, test_folder+'state_15_k5.jpg')

if __name__ == '__main__':
    if os.path.exists('test_file'):
        os.system('rm -rf test_file')
        os.system('mkdir test_file')

    test_5_state(3)
    test_10_state(3)
    test_15_state(3)