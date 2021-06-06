
function showHint(str) {
    if (str.length == 0) {
      document.getElementById("txtHint").innerHTML = "";
      return;
    } else {
      
      var xmlhttp = new XMLHttpRequest();
      xmlhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            
            var table=`<thead><tr>
            <th>Product</th>
            <th>Price</th>
            <th>Qty.</th>
            <th>Last Updated</th>
            <th>Action</th>
            </thead>
          </tr>`;
          var obj=JSON.parse(this.responseText);
          var i;
          for(i in obj){
            table+="<tbody><tr><td>"+obj[i].product+"</td>\
            <td>₹ "+obj[i].price+"</td>\
            <td>"+obj[i].qty+"</td>\
            <td>"+obj[i].date_updated+"</td>";
            table+="<td><a href=delete/"+obj[i].id+">Delete</a>/<a href=update/"+obj[i].id+">Update</a></td</tr></tbody>"
            

          }
          
          document.getElementById("txtHint").innerHTML = table;
         
        }
      };
      xmlhttp.open("GET", "hint/" + str, true);
      xmlhttp.setRequestHeader('Accept', 'application/json');
      xmlhttp.send();
    }
  }





  