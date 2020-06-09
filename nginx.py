import json

class nginx:
    def __init__(self):
        pass
    def conf_reader(self):
        with open("nginx-config-2.txt") as f:
            lines = f.readlines()
            

            upstream_block = list()
            
            for line_number, line in enumerate(lines, 1):
                # this block will search for sections
                line = line.strip().split()
                if "upstream" in line:
                    if "upstream" in line[0]:
                        strating_line = line_number
                        
                        for i in range(strating_line,len(lines)+1):
                            if '}' in lines[i-1]:
                                ending_line = i
                                if ending_line - strating_line == 2:
                                    # if there is only one line in section
                                     
                                    value = lines[ending_line - strating_line -1] + '}'
                                    value = value.replace("\n", "")
                                    value = value.replace("      ","")
                                    upstream_block.append(f"{line[0]} {line[1]} {line[2]} {value}")
                                     
                                else:
                                    # if there is more than one line in section

                                    value =""
                                    block_lines = ending_line - strating_line
                                    for i in range(strating_line,strating_line+block_lines ):
                                        value = value + lines[i]
                                    value = value.replace("\n", "")
                                    value = value.replace("      ","")
                                    upstream_block.append(f"{line[0]} {line[1]} {line[2]} {value}")

                                break

            json_dump = json.dumps(upstream_block)
            with  open('out.txt','w',encoding='utf-8') as myfile:
                myfile.write(json_dump)
                            

                        
                        


            # for line in lines:
            #     line = line.strip().split()
            #     if "upstream" in line:
            #         upstream_block[line[0]] = str(line[1]) + " {" 
                
            # print(upstream_block)

                    


            
        


test = nginx()
test.conf_reader()
