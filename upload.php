<?php

session_start();
$inputFile = $_FILES['inputFile'];
if(isset($_POST['submit'])){
    $countfiles = count($_FILES['inputFile']['name']);
    for($i=0;$i<$countfiles;$i++){
        $filename = $_FILES['inputFile']['name'][$i];
        move_uploaded_file($_FILES['inputFile']['tmp_name'][$i],'upload/'.$filename);
    }
    $myfile = fopen("./flag", "w") or die("Unable to open file!");
    $txt = "1\n";
    fwrite($myfile, $txt);
    fclose($myfile);
    $_SESSION['message'] = "File is successfully uploaded.";
    header("Location: http://localhost:81/index.php");
}

?>