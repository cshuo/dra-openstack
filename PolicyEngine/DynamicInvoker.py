__author__ = 'pike'

action_entry = {
    "migrate_action" : "Arbiter.Migration.MigrateAction"
}


class DynamicInvoker:

    def __init__(self):
        pass

    @staticmethod
    def performAction(actionText):
        (module_name, class_name, action_name) = actionText.rsplit('.', 2)
        module_meta = __import__(module_name, globals(), locals(), [class_name])
        class_meta = getattr(module_meta, class_name)
        classObj = class_meta()
        method = getattr(classObj, action_name)
        method("hello world!")



if __name__ == "__main__":
    actionText = "Arbiter.Action.MigrateAction.migrate"
    DynamicInvoker.performAction(actionText)
