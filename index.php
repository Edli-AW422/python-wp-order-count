<?php
    session_start();
?>
  <?php
    if (isset($_REQUEST['action']) && $_REQUEST['action'] === "checkDone")
    {
      $res = array("result" =>"error","data"=>"");

      echo json_encode($res);
        die();
    }
  ?>
<!DOCTYPE html>
<html>
<head>
    <title>CSV File Upload</title>
    <style type="text/css">

    div.upload-wrapper {
      color: white;
      font-weight: bold;
      display: flex;
    }

    input[type="file"] {
      position: absolute;
      left: -9999px;
    }

    input[type="submit"] {
      border: 3px solid #555;
      color: white;
      background: #666;
      margin: 10px 0;
      border-radius: 5px;
      font-weight: bold;
      padding: 5px 20px;
      cursor: pointer;
    }

    input[type="submit"]:hover {
      background: #555;
    }

    label[for="file-upload"] {
      padding: 0.7rem;
      display: inline-block;
      background: #fa5200;
      cursor: pointer;
      border: 3px solid #ca3103;
      border-radius: 0 5px 5px 0;
      border-left: 0;
    }
    label[for="file-upload"]:hover {
      background: #ca3103;
    }

    span.file-name {
      padding: 0.7rem 3rem 0.7rem 0.7rem;
      white-space: nowrap;
      overflow: hidden;
      background: #ffb543;
      color: black;
      border: 3px solid #f0980f;
      border-radius: 5px 0 0 5px;
      border-right: 0;
    }
    .content {
      margin: auto;
      width: 50%;
      max-width: 200px;
      border: 1px solid green;
      padding: 10px;
    }
    </style>
</head>

<body>


<?php
    if (isset($_SESSION['message']) && $_SESSION['message'] !== "")
    {
      echo '<p class="notification">'.$_SESSION['message'].'</p>';
      unset($_SESSION['message']);
    }
  ?>
<form method="POST" action="./upload.php" class="content" enctype="multipart/form-data">
    <div class="upload-wrapper">
        <span class="file-name">Choose a file...</span>
        <label for="file-upload">Browse<input type="file" multiple id="file-upload" name="inputFile[]"></label>
    </div>

    <input type="submit" name="submit" value="Upload"/>
</form>
<div style="padding: 20px; text-align: center" id="output">Output file : <br>
    <a href="http://111.90.151.228/output.txt">http://111.90.151.228/output.txt</a>
</div>
<script src="./jquery.js"></script>
<script type="text/javascript">
  $(document).ready(function() {
      $("#output").hide();
      function check(){
         $.ajax({
            url: "?action=checkDone",
            dataType: "json",
            type: "GET",
            contentType: "application/javascript; charset=utf-8",
            success: function(msg, status, xhr) {
              console.log(msg)
              if(msg.result == "ok"){
                $("#output").show();
                return;
              }
              setTimeout(check , 3000);
            },
            error: function(xhr, status, error) {
              setTimeout(check , 3000);
              console.log("Result: " + status + " " + error + " " + xhr.status + " " + xhr.statusText)
            }
          });
        }
         check();
  });// $(document).ready(function() 
</script>
</body>
</html>