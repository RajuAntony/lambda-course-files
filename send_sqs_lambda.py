import boto3
import subprocess

# Get the sqs resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='Alertify')

# endless loop
while True:
    # Process messages by printing out body and optional author name
    for message in queue.receive_messages(MessageAttributeNames=['Title', 'SubTitle'], WaitTimeSeconds=20):

        # start building command
        command = 'display notification "{0}"'.format(message.body)

        # add the title to the notification if available
        try:
            title = message.message_attributes.get('Title').get('StringValue')
            command += ' with title "{0}"'.format(title)
        except AttributeError:
            pass

        # add the subtitle to the notification if available
        try:
            subtitle = message.message_attributes.get('SubTitle').get('StringValue')
            command += ' subtitle "{0}"'.format(subtitle)
        except AttributeError:
            pass

        subprocess.call("osascript -e '{0} sound name \"Glass\"'".format(command), shell=True)

        # remove processed message
        message.delete()
