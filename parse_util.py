import re

# get a list of blocks from the given content that start with a string that matches the given regex
def get_blocks(content, start, num_blocks = -1):
    blocks = []
    
    count = 0
    cur = re.search(start, content)

    while cur and (count < num_blocks or num_blocks < 0):
        next_content = content[cur.span()[1]:]
        next = re.search(start, next_content)

        if next:
            blocks.append(content[cur.span()[0]:cur.span()[1] + next.span()[0]])
        else:
            blocks.append(content[cur.span()[0]:])

        cur = next
        content = next_content
        count += 1

    return blocks

# get the next line that matches the given regex
def get_line(regex, lines):
    for line in lines:
        m = re.search(regex, line)

        if (m):
            return m
    
    return None