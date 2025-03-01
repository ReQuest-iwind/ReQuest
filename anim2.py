import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation,PillowWriter
import numpy as np

text1 = 'ReQuest is an information search assistant from technical reports and published papers.'
text2 = 'It has been developed by Giannis Serafeim, for the needs of iWind Renewables.'
text3 = 'The search is carried out in Greek or English, utilizing modern artificial intelligence (AI) tools, like Haystack and available models such as RoBERTa and XLM-RoBERTa.'

def justify_text(text,line_width):
    words = text.split()
    lines = []
    current_line = []
    current_length = 0
    for word in words:
        if current_length + len(word) + len(current_line) <= line_width:
            current_line.append(word)
            current_length += len(word)
        else:
            spaces_needed = line_width - current_length
            for i in range(spaces_needed):
                current_line[i % (len(current_line) - 1)] += ' '
            lines.append(''.join(current_line))
            current_line = [word]
            current_length = len(word)
    lines.append(' '.join(current_line))
    return lines

justified_lines = ['',]+justify_text(text1,48)+['','']+justify_text(text2,48)+['','']+justify_text(text3,48)

fig, ax = plt.subplots()
ax.axis('off')
text_display = ax.text(-0.1,1.0,'',va='top',ha='left',color='#007BFF',fontsize=15,family='DejaVu Sans Mono',wrap=True)

def update(frame):
    if frame>len(' '.join(justified_lines)): frame = len(' '.join(justified_lines))
    full_text = ''
    current_char_count = 0
    for line in justified_lines:
        if current_char_count+len(line)>=frame:
            chars_to_display = frame-current_char_count
            full_text = full_text+line[:chars_to_display]
            break
        full_text = full_text+line+'\n'
        current_char_count = current_char_count+len(line) + 1
    text_display.set_text(full_text)

ani = FuncAnimation(fig,update,frames=481,interval=100)
ani.save('./anim2.gif',writer=PillowWriter(fps=20))
