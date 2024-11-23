import os
import re

def process_res(filename):
    patterns = [
        r"Total dynamic associative search energy/access\s+\(nJ\):\s+(\d+\.\d+)",
        r"Total dynamic read energy/access\s+\(nJ\):\s+(\d+\.\d+)",
        r"Data array: Area \(mm2\):\s+(\d+\.\d+)",
        r"Area efficiency \(Memory cell area/Total area\) - (\d+\.\d+)\s*%",
        r"Tag array: Area \(mm2\):\s+(\d+\.\d+)",
        r"Area efficiency \(Memory cell area/Total area\) - (\d+\.\d+)\s*%"
    ]
    
    results = {}
    
    with open(filename, 'r') as file:
        content = file.read()
        
        # Search for each pattern and extract the float
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                results[pattern] = float(match.group(1))
    
    # print(len(results))
    # energy = 0
    # area = 0
    energy = results[patterns[0]] + results[patterns[1]]
    area = results[patterns[2]] * results[patterns[3]] + results[patterns[4]] * results[patterns[5]]
    
    return area, energy

if __name__ == '__main__':
    os.system('make opt')
    os.system("./cacti -infile sample_config_files/L1cache.cfg  > res1.txt")
    os.system("./cacti -infile sample_config_files/procStRlxCnts.cfg  > res2.txt")
    os.system("./cacti -infile sample_config_files/procUncommittedEpochs.cfg  > res3.txt")
    
    os.system("./cacti -infile sample_config_files/LLCcache.cfg  > res4.txt")
    os.system("./cacti -infile sample_config_files/dirstRlxCnts.cfg  > res5.txt")
    os.system("./cacti -infile sample_config_files/dirNotifyCnts.cfg  > res6.txt")
    os.system("./cacti -infile sample_config_files/dirMaxCommittedEpochs.cfg  > res7.txt")
    
    proc_baseline_area, proc_baseline_energy = process_res('res1.txt')
    proc_area = 0
    proc_energy = 0
    for i in range(2, 4):
        a, e = process_res(f'res{i}.txt')
        proc_area += a
        proc_energy += e
    proc_area /= proc_baseline_area
    proc_energy /= proc_baseline_energy
    
    dir_baseline_area, dir_baseline_energy = process_res('res4.txt')
    dir_area = 0
    dir_energy = 0
    for i in range(5, 8):
        a, e = process_res(f'res{i}.txt')
        dir_area += a
        dir_energy += e
    dir_area /= dir_baseline_area
    dir_energy /= dir_baseline_energy    
    
    print(f'proc area:{proc_area} energy:{proc_energy}')
    print(f'dir area:{dir_area} energy:{dir_energy}')