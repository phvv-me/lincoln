import importlib
import logging

# Set up logging
logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class LambdaHandler:

    @staticmethod
    def import_module_and_get_function(whole_function):
        """
        Given a modular path to a function, import that module
        and return the function.
        """
        module, function = whole_function.rsplit('.', 1)
        app_module = importlib.import_module(module)
        app_function = getattr(app_module, function)

        logger.debug(f"function {app_function} from module {app_module} was imported")
        return app_function

    @classmethod
    def lambda_handler(cls, event, context):
        try:
            return cls().handler(event, context)
        except Exception:
            logger.exception(msg='Failed to process exception via custom handler.')
            raise

    def handler(self, event, context):
        result = None

        # This is the result of Cloudwatch scheduled event.
        if event.get('detail-type') == 'Scheduled Event':

            whole_function = event['resources'][0].split('/')[-1].split('-')[-1]

            # This is a scheduled function.
            if '.' in whole_function:
                app_function = self.import_module_and_get_function(whole_function)

                # Execute the function!
                result = app_function(event, context)
                logger.debug(f"{app_function} called for event {event}")

        # This is a direct invocation.
        else:
            pass

        logger.debug(f"returned {result} for event {event}")
        return result


def handler(event, context):
    return LambdaHandler.lambda_handler(event, context)