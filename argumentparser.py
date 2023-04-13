def difference(op1: list, op2: list):
    return [el for el in op1 if el not in op2]

def inter(op1: list, op2: list):
    return [el for el in op1 if el in op2]


def parse_arguments(args: list[str],flags: list[str] =[],prefix: str = '--'):
    parsed_args = {}
    free_args = []
    temp_arg_name = None
    for flag in inter(args, flags):
        parsed_args[flag] = ""
    #remove all flags from paired args
    paired_args = difference(args, flags)
    for arg in paired_args:
        if arg.startswith(prefix):
            if temp_arg_name != None: 
                raise Exception(f"{arg} is not a valid value for {temp_arg_name}")
            else: 
                temp_arg_name = arg
        elif temp_arg_name != None:
            parsed_args[temp_arg_name] = arg
            temp_arg_name = None
        else:
            free_args.append(arg)
        
    
    parsed_args['freeArgs'] = free_args
    return parsed_args
