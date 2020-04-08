# Original idea found here: https://www.sitepoint.com/how-built-pure-css-crossword-puzzle/
# With codepen example here: https://codepen.io/adrianroworth/pen/OpeyZq?editors=1100

print("<html>")
print("<head><link rel='stylesheet' href='crossword.css'><script src='https://ajax.aspnetcdn.com/ajax/jQuery/jquery-3.4.1.min.js'></script><script src='crossword.js' type='text/javascript'></script></head>")

label_map = {}

f = open("crossword.txt", "r")
line = f.readline().strip() # title
print("<header>")
print("<h1>" + line + "</h1>")
line = f.readline().strip() # flavor text
print("<p class='flavor'><i>" + line + "</i></p>");
print("</header>")
author = f.readline().strip() # author

row = 1
print("<div class='crossword-board-container'>")
print("\t<div class='crossword-board'>")
labels_div = "\t<div class='crossword-board crossword-board--labels'>\n"
while(line):
        line = f.readline()
        line = line.strip("\n")
        col = 1
        for char in line:
                id = "'item%s-%s'" % (str(row), str(col))
                if char != " ": # is a space to be filled in
                        print("\t\t<input id=%s class='crossword-board__item' type='text' minlength='1' maxlength='1' value='' required='required' />" % id)
                        if char != "x": # is a label
                                id = str(ord(char)-64)
                                label_map[id] = (str(row), str(col))
                                style = "grid-column: " + str(col) + "/" + str(col) + "; grid-row: " + str(row) + "/" + str(row) + ";"
                                labels_div += "\t\t<span id='label-%s' class='crossword-board__item-label crossword-board__item-label--%s' style='%s'><span class='crossword-board__item-label-text'>%s</span></span>\n" % (id, id, style, id)
                else: # is a black square
                        print("\t\t<span class='crossword-board__item--blank' id=%s></span>" % id)
                col += 1
        row += 1
print("\t</div>")
f.close()

labels_div += "\t</div>"
print(labels_div)

print("\t<div class='crossword-clues'>")
print("\t\t<p><i>Double-click a clue to mark as completed</i></p>")
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
                num = line.split(" ")[0]
                clue = " ".join(line.split(" ")[1:])
                print("\t\t\t<dd class='crossword-clues__list-item crossword-clues__list-item--%s-%s' data-number='%s' data-row='%s' data-col='%s'>%s</dd>" % (dir, num, num, label_map[num][0], label_map[num][1], clue))

print("\t\t</dl>")
print("\t\t<div><button class='clear'>Clear All</button></div>")
print("\t</div>")
print("</div>")
print("<footer><p>" + author + "</p></footer>")
print("</html>")
