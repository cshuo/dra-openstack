__author__ = 'pike'

action_entry = {
    "arbiter.migrate" : "Arbiter.Arbiter.ArbiterProxy.migrate"
}


class DynamicInvoker:

    def __init__(self):
        pass

    @staticmethod
    def performAction(action):
        action = action_entry[action]
        (module_name, class_name, action_name) = action.rsplit('.', 2)
        module_meta = __import__(module_name, globals(), locals(), [class_name])
        class_meta = getattr(module_meta, class_name)
        classObj = class_meta()
        method = getattr(classObj, action_name)
        method()



if __name__ == "__main__":
    action = "arbiter.migrate"
    DynamicInvoker.performAction(action)
