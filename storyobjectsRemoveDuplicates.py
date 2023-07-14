from storyobjects import story_objects
from collections import OrderedDict

# remove duplicates while preserving order
data_list = list(OrderedDict.fromkeys(story_objects))

# write back the unique list to the file
with open('storyobjects.py', 'w') as file:
    file.write('data_list = [\n')
    for item in data_list:
        file.write('    "{}",\n'.format(item))
    file.write(']\n')