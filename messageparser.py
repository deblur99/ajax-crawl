with open('./message.txt', 'r') as f:
    messages = f.readlines()

with open('./messages_with_format.json', 'w') as f:
    f.write('[\n')
    for idx, message in enumerate(messages):
        if idx < len(messages) - 1:
            message = '\t\"' + message.rstrip() + '\",\n'
            f.write(message)
        else:
            message = '\t\"' + message.rstrip() + '\"\n'
            f.write(message)
    f.write(']')
