// In long descclassnames, allow word-wrapping on periods.

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".descclassname").forEach(function (element) {
        // Collect the text nodes first: replacing them as we walk would
        // disturb the walker.
        var walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT);
        var textNodes = [];
        while (walker.nextNode()) {
            textNodes.push(walker.currentNode);
        }
        textNodes.forEach(function (textNode) {
            if (!textNode.data.includes(".")) {
                return;
            }
            var fragment = document.createDocumentFragment();
            textNode.data.split(".").forEach(function (part, index) {
                if (index > 0) {
                    fragment.append(".", document.createElement("wbr"));
                }
                fragment.append(part);
            });
            textNode.replaceWith(fragment);
        });
    });
});
