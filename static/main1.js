
function showPro() {
    var p=document.getElementById('product').value
    var q=document.getElementById('qty').value

    if (p.length == 0) {
        document.getElementById("msg").innerHTML = "";
        return;
    } else {

        var xmlhttp = new XMLHttpRequest();
        xmlhttp.onreadystatechange = function () {
            if (this.readyState == 4 && this.status == 200) {


                //var obj = JSON.parse(this.responseText);
                if (this.responseText=="Product Already In Database!"){
                    clr()
                }


            }

            document.getElementById("msg").innerHTML = this.responseText;

        }
    };
    xmlhttp.open("GET", "product_check?q="+p+"&q1="+q, true);
    
    xmlhttp.send();
}

function clr(){
    var p=document.getElementById('product').value=""
    var q=document.getElementById('qty').value=""

}
  





