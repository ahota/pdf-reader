overlay_data = null;

// based on: https://gist.github.com/fcingolani/3300351
function renderPDF(url, container, scale) {

    if(!scale)
        var scale = 1.5;

    // render a single page from the PDF into its own canvas,
    // then append that canvas to the container
    // This means that the HTML only needs a container div and
    // no canvas elements
    function renderPage(page) {
        console.log(page);
        var viewport = page.getViewport(scale);
        var canvas = document.createElement('canvas');
        var context = canvas.getContext('2d');
        var renderContext = {
            canvasContext: context,
            viewport: viewport
        };

        canvas.height = viewport.height;
        canvas.width = viewport.width;

        // set the container width so that the pages don't render side-by-side
        if(page.pageIndex == 0) {
            container.style.height = canvas.height.toString() + "px";
            container.style.width = canvas.width.toString() + "px";
            container.style.margin = "10px auto";
        }

        container.appendChild(canvas);

        page.render(renderContext);
    }

    // iteratively render all the pages in the PDF
    function renderPages(doc) {
        // 1-based indexing >_>
        for(var p = 1; p <= doc.numPages; p++)
            doc.getPage(p).then(renderPage);
    }

    PDFJS.disableWorker = true;
    PDFJS.getDocument(url).then(renderPages);
}

function setupOverlay(canvas) {
    var overlay = document.getElementById('content');
    overlay.style.height = canvas.height.toString() + "px";
    overlay.style.width = canvas.width.toString() + "px";
    overlay.style.margin = "10px auto";
    $.ajax({
        type: "GET",
        url: "/overlay_info",
        success: function(result) {
            overlay_data = $.parseJSON(result);
            console.log(overlay_data);
            var box = document.createElement("div");
            box.setAttribute("class", "overlay-box");
            box.style.left = `${overlay_data[0].bbox[0]}px`;
            box.style.bottom = `${overlay_data[0].bbox[1]}px`;
            box.style.width = `${overlay_data[0].bbox[2] - overlay_data[0].bbox[0]}px`;
            box.style.height = `${overlay_data[0].bbox[3] - overlay_data[0].bbox[1]}px`;
            box.setAttribute("data-intro", overlay_data[0].data);
            if(overlay_data[0].bbox[0] < (viewport.width / 2)) {
                box.setAttribute("data-position", "left");
            }
            else {
                box.setAttribute("data-position", "right");
            }
            box.setAttribute("data-toggle", "chardinjs");
            //var box_data = document.createElement("div");
            //box_data.setAttribute("class", "overlay-box-data");
            //box_data.innerHTML = overlay_data[0].data;
            //box.appendChild(box_data);
            overlay.appendChild(box);
            $('.overlay-box').on("click", function(ev) {
                ev.preventDefault();
                console.log("hey");
                $('body').chardinJs('toggle');
            });
        },
        error: function(result) {
        }
    });
}

$(document).ready(function() {
    var url = '/pdfs/last.pdf';
    renderPDF(url, document.getElementById('content'));
});
