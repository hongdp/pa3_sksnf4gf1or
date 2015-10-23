

function makeCaptionRequest(picid, cb) {
  qwest.get('/secretkey/pa3/pic/caption?id=' + picid)
    .then(function(xhr, resp) {
      cb(resp);
    });
}

// caption.js bottom function
//query data store for latest fetch data
function initCaption(picid) {
  var caption = document.getElementById("caption");
  var captionBinding = new Caption(caption, picid);

  makeCaptionRequest(picid, function(resp) {
    captionBinding.change(resp['caption']);
  });

  setInterval(function() {
   makeCaptionRequest(picid, function(resp) {
      captionBinding.change(resp['caption']);
    });
  }, 7000);
}
