
def get_automation_object(file):
    eval(f'from {file} import Automation')
    return Automation