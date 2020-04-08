var typingDirection = "across";
var fShift = false;

$(document).ready(function() {
        // When a clue is double clicked, cross it out (or un-cross it)
        $("dd").dblclick(function() {
                $(this).toggleClass("strikethrough");
        });

        // When a clue is hovered, highlight its squares in the grid
        $("dd").hover(function() {
                var label = $("#label-" + $(this).data("number"));
                var row = parseInt($(label).css("grid-row-start"));
                var col = parseInt($(label).css("grid-column-start"));

                var across = this.className.indexOf("across") >= 0;
                var square = $("#item" + row.toString() + "-" + col.toString());
                while (!$(square).hasClass("crossword-board__item--blank")) {
                        $(square).addClass("marked")

                        if (across) col += 1;
                        else row += 1
                        square = $("#item" + row.toString() + "-" + col.toString());
                }
        }, function() {
                $(".crossword-board__item").removeClass("marked");
        });

        $("dd").click(function() {
                var label = $("#label-" + $(this).data("number"));
                var row = parseInt($(label).css("grid-row-start"));
                var col = parseInt($(label).css("grid-column-start"));

                var across = this.className.indexOf("across") >= 0;
                var square = $("#item" + row.toString() + "-" + col.toString());
                if (!$(square).hasClass("crossword-board__item--blank")) {
                        $(square).focus();
                }
        });

        function FindLabelVertical(row, col) {
                var square = $("#item" + (row-1).toString() + "-" + col.toString());

                while (!$(square).hasClass("crossword-board__item--blank")) {
                        row -= 1;
                        square = $("#item" + (row-1).toString() + "-" + col.toString());
                }
                return "*[data-row='" + row.toString() + "'][data-col='" + col.toString() + "']";
        }

        function FindLabelHorizontal(row, col) {
                square = $("#item" + row.toString() + "-" + (col-1).toString());
                while (!$(square).hasClass("crossword-board__item--blank")) {
                        col -= 1;
                        square = $("#item" + row.toString() + "-" + (col-1).toString());
                }
                return "*[data-row='" + row.toString() + "'][data-col='" + col.toString() + "']";
        }

        // When an input box is selected, the appropriate clue(s) are highlighted too
        $(".crossword-board__item").focus(function() {
                var label = $(this).attr("id");
                var row = parseInt(label.split("-")[0].substr(4));
                var col = parseInt(label.split("-")[1]);

                // Check up for a label
                label = FindLabelVertical(row, col);
                $(label).addClass("marked");

                // Check to the left for a label
                label = FindLabelHorizontal(row, col);
                $(label).addClass("marked");
        });
        $(".crossword-board__item").focusout(function() {
                $(".crossword-clues__list-item").removeClass("marked");
        });

        $(".clear").click(function() {
                $(".crossword-board__item").each(function() {
                        $(this).val("");
                });
        });

        // When the user opens the page, load any existing progress
//        $(".crossword-board__item").each(function() {
//                var value = $(this).attr("id");
//                if (localStorage.getItem(value)) {
//                        $(this).val(localStorage.getItem(value));
//                }
//        });


        // When the user leaves the page, store the progress
//        $(window).bind("beforeunload", function(e) {
//                $(".crossword-board__item").each(function() {
//                        localStorage.setItem($(this).attr("id"), $(this).val());
//                });
//        });

        // Handle arrow keys
        function move(elem, drow, dcol) {
                var label = $(elem).attr("id");
                var row = parseInt(label.split("-")[0].substr(4)) + drow;
                var col = parseInt(label.split("-")[1]) + dcol;

                var newitem = $("#item" + row + "-" + col);
                if (newitem && !$(newitem).hasClass("crossword-board__item--blank")) {
                        $(newitem).focus();
                        return true;
                }

                return false;
        }

        $(".crossword-board__item").on("keydown", function(e) {
                if (e.keyCode == 37) { // left
                        move(this, 0, -1);
                        typingDirection = "across";
                }
                else if (e.keyCode == 38) { // up
                        move(this, -1, 0);
                        typingDirection = "down";
                }
                else if (e.keyCode == 39) { // right
                        move(this, 0, 1);
                        typingDirection = "across";
                }
                else if (e.keyCode == 40) { // down
                        move(this, 1, 0);
                        typingDirection = "down";
                }
                else if (e.keyCode == 9) { // tab
                        var label = $(this).attr("id");
                        var row = parseInt(label.split("-")[0].substr(4));
                        var col = parseInt(label.split("-")[1]);

                        var label;
                        if (typingDirection === "across") {
                                label = FindLabelHorizontal(row, col);
                                if ($(label).length === 0) {
                                        label = FindLabelVertical(row, col);
                                }
                        }
                        else { // typingDirection === "down"
                                label = FindLabelVertical(row, col);
                                if ($(label).length === 0) {
                                        label = FindLabelHorizontal(row, col);
                                }
                        }
                        if ($(label).length !== 0) {
                                var next = parseInt($(label).data("number")) + (fShift ? -1 : 1);

                                if ($("*[data-number='" + next + "']").length === 0) {
                                        if (!fShift) next = 1;
                                        else {
                                                var nums = $("dd").map(function() {
                                                        return $(this).data("number");
                                                }).get();
                                                next = Math.max.apply(Math, nums);
                                        }
                                }

                                next = "*[data-number='" + next + "']";
                                $("#item" + $(next).data("row") + "-" + $(next).data("col")).focus();

                                if ($(next).attr("class").indexOf("across") === -1)
                                        typingDirection = "down";
                                else
                                        typingDirection = "across";

                                e.preventDefault();
                        }
                }
                else if ($(this).val() && (e.keyCode >= 65 && e.keyCode <= 90)) { // clear existing letter for new one
                        $(this).val("");
                }
        });

        $(".crossword-board__item").on("keypress", function(e) {
                if (e.which >= 97 && e.which <= 122) { // A-Z
                        $(this).val($(this).val().toUpperCase());
                        if (typingDirection === "across") {
                                if (!move(this, 0, 1)) {
                                        if (move(this, 1, 0)) {
                                                typingDirection = "down";
                                        }
                                }
                        }
                        else { // typingDirection === "down"
                                if (!move(this, 1, 0)) {
                                        if (move(this, 0, 1)) {
                                                typingDirection = "across";
                                        }
                                }
                        }
                }
                else { // don't allow other characters
                        var currVal = $(this).val();
                        if (currVal && (currVal.charCodeAt(0) < 65 || currVal.charCodeAt(0) > 90)) {
                                $(this).val("");
                        }
                }
        });

        $(document).on("keyup keydown", function(e) {fShift = e.shiftKey} );
});
