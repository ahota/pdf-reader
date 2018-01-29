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
        var viewport = page.getViewport(scale);

        var overlayContainer = document.createElement('div');
        overlayContainer.setAttribute('class', 'overlay-container');
        //overlayContainer.style.zIndex = "10";

        var pageContainer = document.createElement('div');
        pageContainer.setAttribute('class', 'page-container');

        var canvas = document.createElement('canvas');
        canvas.setAttribute('class', 'page-canvas');
        canvas.style.zIndex = "-1000";

        var context = canvas.getContext('2d');
        var renderContext = {
            canvasContext: context,
            viewport: viewport
        };

        canvas.height = viewport.height;
        canvas.width = viewport.width;
        overlayContainer.style.height = canvas.height.toString() + "px";
        overlayContainer.style.width = canvas.width.toString() + "px";
        pageContainer.style.height = canvas.height.toString() + "px";
        pageContainer.style.width = canvas.width.toString() + "px";

        // set the document container width so that the pages don't render
        // side-by-side
        if(page.pageIndex == 0) {
            container.style.width = canvas.width.toString() + "px";
            container.style.margin = "10px auto";
        }

        container.appendChild(pageContainer);
        pageContainer.appendChild(overlayContainer);
        pageContainer.appendChild(canvas);

        page.render(renderContext).then(function() {
            setupOverlay(page.pageNumber, scale);
        },
        function() {
            console.log("me got error");
        });
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

function setupOverlay(pageNum, scale) {
    for(var index = 0; index < overlay_data.length; index++) {
        // check if there is a watermarked image on this page
        console.log(index);
        if(overlay_data[index].page == pageNum) {
            console.log("adding to page " + pageNum.toString());
            var pageOverlay = document.getElementsByClassName('overlay-container')[pageNum];

            var box = document.createElement("img");
            box.setAttribute("class", "overlay-box");
            box.setAttribute("src", overlay_data[index].image_data);
            var scaled_bbox = [];
            overlay_data[index].bbox.forEach(function(element) {
                scaled_bbox.push(element * scale);
            });
            box.style.left = scaled_bbox[0] + "px";
            box.style.bottom = scaled_bbox[1] + "px";
            box.style.width = (scaled_bbox[2] - scaled_bbox[0]) + "px";
            box.style.height = (scaled_bbox[3] - scaled_bbox[1]) + "px";
            box.setAttribute("data-intro", overlay_data[index].data);
            if(overlay_data[index].bbox[0] < (parseInt(pageOverlay.style.width) / 2)) {
                box.setAttribute("data-position", "left");
            }
            else {
                box.setAttribute("data-position", "right");
            }
            //box.style.zIndex = "11";

            // add Chardin.JS toggle event handler to all boxes
            box.onclick = toggleChardinJS;

            pageOverlay.appendChild(box);
        }
    }
}

function toggleChardinJS() {
    $('body').chardinJs('toggle');
}

$(document).ready(function() {
    var url = '/pdfs/last.pdf';
    $.ajax({
        type: "GET",
        url: "/overlay_info",
        success: function(result) {
            overlay_data = $.parseJSON(result);
            renderPDF(url, document.getElementById('content'));
        },
        error: function(result) {
        }
    });
});
