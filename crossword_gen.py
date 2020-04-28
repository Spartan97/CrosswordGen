# Original idea found here: https://www.sitepoint.com/how-built-pure-css-crossword-puzzle/
# With codepen example here: https://codepen.io/adrianroworth/pen/OpeyZq?editors=1100

print("<html>")
print("<head><link rel='stylesheet' href='crossword.css'><script src='https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.4.1.min.js'></script><script src='crossword.js' type='text/javascript'></script></head>")

label_map = {}
extraction_map = {}

f = open("crossword.txt", "r")
line = f.readline().strip() # title
print("<header>")
print("<h1>" + line + "</h1>")
line = f.readline().strip() # flavor text
print("<p class='flavor'><i>" + line + "</i></p>");
print("</header>")
author = f.readline().strip() # author

grid = []
line = f.readline().strip("\n")
cols = len(line)
while(line):
        grid.append(list(line))
        line = f.readline().strip("\n")
        if len(line) == 0:
                break
        elif len(list(line)) != cols:
                print("Invalid grid")
                quit()

print("<div class='crossword-board-container'>")
print("\t<div class='crossword-board'>")
labels_div = "\t<div class='crossword-board crossword-board--labels'>\n"
extraction_div = "\t<div class='crossword-board crossword-board--extraction'>\n"

next_label = 1
for row in range(len(grid)):
        for col in range(len(grid[0])):
                id = "'item%s-%s'" % (str(row+1), str(col+1))
                char = grid[row][col]
                if char != " ": # is a space to be filled in
                        print("\t\t<input id=%s class='crossword-board__item' type='text' minlength='1' maxlength='1' value='' required='required' />" % id)
                        if (row > 0 and grid[row-1][col] == " " and row < len(grid)-1 and grid[row+1][col] != " ") or (col > 0 and grid[row][col-1] == " " and col < len(grid[0])-1 and grid[row][col+1] != " "): # is a label
                                label_map[next_label] = (str(row+1), str(col+1))
                                style = "grid-column: " + str(col+1) + "/" + str(col+1) + "; grid-row: " + str(row+1) + "/" + str(row+1) + ";"
                                labels_div += "\t\t<span id='label-%s' class='crossword-board__item-label crossword-board__item-label--%s' style='%s'><span class='crossword-board__item-label-text'>%s</span></span>\n" % (next_label, next_label, style, next_label)
                                next_label += 1

                        if char >= "A" and char <= "Z": # extaction labels
                                ordchar = str(ord(char)-64)
                                extraction_map[ordchar] = (str(row+1), str(col+1));
                                style = "grid-column: " + str(col+1) + "/" + str(col+1) + "; grid-row: " + str(row+1) + "/" + str(row+1) + ";"
                                extraction_div += "\t\t<span id='extraction-%s' class='crossword-board__item-extraction crossword-board__item-extraction--%s' style='%s'><span class='crossword-board__item-extraction-text'>%s</span></span>\n" % (ordchar, ordchar, style, ordchar)
                else: # is a black square
                        print("\t\t<span class='crossword-board__item--blank' id=%s></span>" % id)

print("\t</div>")
f.close()

labels_div += "\t</div>"
extraction_div += "\t</div>"
print(labels_div)
print(extraction_div)

print("\t<div class='crossword-clues'>")
print("\t\t<p><i>Right-click a clue to mark as completed</i></p>")
print("\t\t<dl class='crossword-clues__list crossword-clues__list--across'>")
print("\t\t\t<dt class='crossword-clues__list-title'>Across</dt>")
f = open("clues.txt", "r")
dir = "across"
for line in f:
        line = line.strip()
        if line == "across":
                pass
        elif line == "down":
                dir = "down"
                print("\t\t</dl>")
                print("\t\t<dl class='crossword-clues__list crossword-clues__list--down'>")
                print("\t\t\t<dt class='crossword-clues__list-title'>Down</dt>")
        elif line:
                num = int(line.split(" ")[0])
                clue = "".join(line.split(" ")[1:])
                print("\t\t\t<dd class='crossword-clues__list-item crossword-clues__list-item--%s-%s' data-number='%s' data-row='%s' data-col='%s'>%s</dd>" % (dir, num, num, label_map[num][0], label_map[num][1], clue))

print("\t\t</dl>")
print("\t\t<div><button class='clear'>Clear All</button></div>")

print("\t\t<div class='extraction' style='margin-top:16px; font-size:48px'>")
for key in sorted(extraction_map.keys(), key = lambda k:(int(k))):
        value = extraction_map[key]
        print("\t\t\t<span style='position:relative'><span id='extraction%s-%s' class='crossword-extraction__value' data-number='%s' data-row='%s' data-col='%s'>_</span><span id='extraction-label' style='margin-top:175%%;left:0%%;text-align:center;width:100%%;position:absolute;font-size:14px;color:red'>%s</span></span>" % (value[0], value[1], key, value[0], value[1], key));

print("\t\t</div>")
print("\t</div>")
print("</div>")
print("<footer><p>" + author + "</p></footer>")
print("</html>")
