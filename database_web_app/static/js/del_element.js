document.addEventListener("DOMContentLoaded", bindButtons);

function bindButtons() {
  document.getElementById("selTitleSearch").addEventListener("click", function(event){
    document.getElementById("delDevSearch").style.display = "none";
    document.getElementById("delPlatSearch").style.display = "none";
    document.getElementById("delFranchiseSearch").style.display = "none";

    document.getElementById("delTitleSearch").style.display = "block";

    document.getElementById("delSuccessful").style.display = "none"
  });

  document.getElementById("selDevSearch").addEventListener("click", function(event){
    document.getElementById("delTitleSearch").style.display = "none";
    document.getElementById("delPlatSearch").style.display = "none";
    document.getElementById("delFranchiseSearch").style.display = "none";

    document.getElementById("delDevSearch").style.display = "block";

    document.getElementById("delSuccessful").style.display = "none"
  });

  document.getElementById("selPlatSearch").addEventListener("click", function(event){
    document.getElementById("delTitleSearch").style.display = "none";
    document.getElementById("delDevSearch").style.display = "none";
    document.getElementById("delFranchiseSearch").style.display = "none";

    document.getElementById("delPlatSearch").style.display = "block";

    document.getElementById("delSuccessful").style.display = "none"
  });

  document.getElementById("selFranchiseSearch").addEventListener("click", function(event){
    document.getElementById("delTitleSearch").style.display = "none";
    document.getElementById("delDevSearch").style.display = "none";
    document.getElementById("delPlatSearch").style.display = "none";

    document.getElementById("delFranchiseSearch").style.display = "block";

    document.getElementById("delSuccessful").style.display = "none"
  });

  document.getElementById("searchTitleButton").addEventListener("click", function(event) {
    var req = new XMLHttpRequest();
    
    var payload = {"action": "searchTitle",
                    "titleName": document.getElementById('searchTitleName').value,
                    "titlePlatID": document.getElementById('searchTitlePlatID').value, 
                    "titleFromDate": document.getElementById('searchTitleFromDate').value, 
                    "titleToDate": document.getElementById('searchTitleToDate').value, 
                    "titleGenre": document.getElementById('searchTitleGenre').value, 
                    "titleFranchiseID": document.getElementById('searchTitleFranchiseID').value,
                    "titleDevID": document.getElementById('searchTitleDevID').value,
                    "titleESRB": document.getElementById('searchTitleESRB').value};

    req.open('POST', '/delete', true);
    req.setRequestHeader('Content-Type', 'application/json');

    req.addEventListener('load', function(){
      if (req.status >= 200 && req.status < 400) {
        res = JSON.parse(req.responseText);

        // clear out current search result table rows
        var prevTableRows = document.getElementsByClassName('searchResultRow');
        while (prevTableRows[0]) {
          prevTableRows[0].remove();
        }
        searchTable = document.getElementById("searchResultTable")
        
        // add appropriate header rows for Titles table
        header_tr = document.createElement('tr');
        header_tr.setAttribute('class', 'searchResultRow');
        
        header_elements = ["Title", "Platforms", "Release Date<br/>(North America)", "Genre",
                            "Franchise", "Developer", "ESRB Rating", "Delete"];
        for (var i = 0; i < header_elements.length; i++) {
          header_td = document.createElement('th');
          if (i != 2) {
            header_td.textContent = header_elements[i];
          } else {
            header_td.innerHTML = header_elements[i];
          }
          header_tr.appendChild(header_td);
        }
        searchTable.appendChild(header_tr);

        // add each row into the search result table
        for (var i = 0; i < res.length; i++) {
          title_tr = document.createElement('tr');
          title_tr.setAttribute('class', 'searchResultRow');
          title_tr.setAttribute('id', res[i][0]);
          
          // title name cells
          td_cell = document.createElement('td');
          td_cell.textContent = res[i][1];
          title_tr.appendChild(td_cell);

          // platforms cells
          td_cell = document.createElement('td');
          plat_list = document.createElement('ul');
          plat_list.setAttribute('class', 'platformList');
          for (var j = 0; j < res[i][7].length; j++) {
            plat_item = document.createElement('li');
            plat_item.textContent = res[i][7][j];
            plat_list.appendChild(plat_item);
          }
          td_cell.appendChild(plat_list);
          title_tr.appendChild(td_cell);

          // genre, franchise, dev, esrb cells
          for (var j = 2; j < 7; j++) {
            td_cell = document.createElement('td');
            td_cell.textContent = res[i][j]
            title_tr.appendChild(td_cell);
          }

          // add delete button
          button_td = document.createElement('td');
          del_button = document.createElement('button');
          del_button.setAttribute('type', 'button');
          del_button.setAttribute('class', 'titleDelButton');
          del_button.setAttribute('value', res[i][0]);
          del_button.textContent = "Delete"
          button_td.appendChild(del_button);
          title_tr.appendChild(button_td);

          searchTable.appendChild(title_tr);
        }

        // rebind the new delete buttons to trigger delete query

        bind_delete_buttons();

      } else {
        console.log("Error in network request: " + req.statusText);
    }});

    req.send(JSON.stringify(payload));
  });

  document.getElementById("searchDevButton").addEventListener("click", function(event) {
    var req = new XMLHttpRequest();

    var payload = {"action": "searchDev",
                    "devName": document.getElementById('searchDevName').value,
                    "devCountry": document.getElementById('searchDevCountry').value, 
                    "devFromDate": document.getElementById('searchDevFromDate').value, 
                    "devToDate": document.getElementById('searchDevToDate').value};

    req.open('POST', '/delete', true);
    req.setRequestHeader('Content-Type', 'application/json');

    req.addEventListener('load', function(){
      if (req.status >= 200 && req.status < 400) {
        res = JSON.parse(req.responseText);

        // clear out current search result table rows
        var prevTableRows = document.getElementsByClassName('searchResultRow');
        while (prevTableRows[0]) {
          prevTableRows[0].remove();
        }
        searchTable = document.getElementById("searchResultTable")
        
        // add appropriate header rows for Developer Studios table
        header_tr = document.createElement('tr');
        header_tr.setAttribute('class', 'searchResultRow');
        header_elements = ["Developer Studio", "Country", "Date Founded", "Delete?"];
        for (var i = 0; i < header_elements.length; i++) {
          header_th = document.createElement('th');
          header_th.textContent = header_elements[i];
          header_tr.appendChild(header_th);
        }
        searchTable.appendChild(header_tr);

        // add each row into the search result table
        for (var i = 0; i < res.length; i++) {
          title_tr = document.createElement('tr');
          title_tr.setAttribute('class', 'searchResultRow');
          title_tr.setAttribute('id', res[i][0]);
          
          // name, country, date founded cells
          for (var j = 1; j < 4; j++) {
            td_cell = document.createElement('td');
            td_cell.textContent = res[i][j];
            title_tr.appendChild(td_cell);
          }
  
          // add delete button
          button_td = document.createElement('td');
          del_button = document.createElement('button');
          del_button.setAttribute('type', 'button');
          del_button.setAttribute('class', 'devDelButton');
          del_button.setAttribute('value', res[i][0]);
          del_button.textContent = "Delete"
          button_td.appendChild(del_button);
          title_tr.appendChild(button_td);

          searchTable.appendChild(title_tr);
        }

        // rebind the new delete buttons to trigger delete query
        bind_delete_buttons();

      } else {
        console.log("Error in network request: " + req.statusText);
    }});

    req.send(JSON.stringify(payload));
  });

  document.getElementById("searchPlatButton").addEventListener("click", function(event) {
    var req = new XMLHttpRequest();

    var platInProd = Array.from(document.getElementsByClassName("searchPlatInProd"));
    if (platInProd[0].checked) {
      platInProd = "Yes";
    } else if (platInProd[1].checked) {
      platInProd = "No";
    } else {
      platInProd = "";
    }

    var payload = {"action": "searchPlat",
            "platName": document.getElementById('searchPlatName').value,
            "platFromDate": document.getElementById('searchPlatFromDate').value, 
            "platToDate": document.getElementById('searchPlatToDate').value, 
            "platDev": document.getElementById('searchPlatDev').value,
            "platInProd": platInProd};
    req.open('POST', '/delete', true);
    req.setRequestHeader('Content-Type', 'application/json');            

    req.addEventListener('load', function(){
      if (req.status >= 200 && req.status < 400) {
        res = JSON.parse(req.responseText);

        // clear out current search result table rows
        var prevTableRows = document.getElementsByClassName('searchResultRow');
        while (prevTableRows[0]) {
          prevTableRows[0].remove();
        }

        searchTable = document.getElementById("searchResultTable")
        
        // add appropriate header rows for Platforms table
        header_tr = document.createElement('tr');
        header_tr.setAttribute('class', 'searchResultRow');
        
        header_elements = ["Platform", "Release Date<br/>(North America)", "Developer", "In Prduction", "Delete?"];
        for (var i = 0; i < header_elements.length; i++) {
          header_th = document.createElement('th');
          if (i != 1) {
            header_th.textContent = header_elements[i];
          } else {
            header_th.innerHTML = header_elements[i];
          }
          header_tr.appendChild(header_th);
        }
        searchTable.appendChild(header_tr);

        // add each row into the search result table
        for (var i = 0; i < res.length; i++) {
          title_tr = document.createElement('tr');
          title_tr.setAttribute('class', 'searchResultRow');
          title_tr.setAttribute('id', res[i][0]);
          
          // name, release, dev cells
          for (var j = 1; j < 4; j++) {
            td_cell = document.createElement('td');
            td_cell.textContent = res[i][j];
            title_tr.appendChild(td_cell);
          }

          // in production cell
          inProd_val = document.createElement('td');
          if (res[i][4]) {
            inProd_val.textContent = "Y"
          } else {
            inProd_val.textContent = "N"
          }
          title_tr.appendChild(inProd_val);

          // add delete button
          button_td = document.createElement('td');
          del_button = document.createElement('button');
          del_button.setAttribute('type', 'button');
          del_button.setAttribute('class', 'platDelButton');
          del_button.setAttribute('value', res[i][0]);
          del_button.textContent = "Delete"
          button_td.appendChild(del_button);
          title_tr.appendChild(button_td);

          searchTable.appendChild(title_tr);
        }

        // rebind the new delete buttons to trigger delete query
        bind_delete_buttons();

      } else {
        console.log("Error in network request: " + req.statusText);
    }});

    req.send(JSON.stringify(payload));
  });

  document.getElementById("searchFranchiseButton").addEventListener("click", function(event) {
    var req = new XMLHttpRequest();
    var payload = {"action": "searchFranchise",
            "franchiseName": document.getElementById('searchFranchiseName').value,
            "franchiseDev": document.getElementById('searchFranchiseDev').value};
    req.open('POST', '/delete', true);
    req.setRequestHeader('Content-Type', 'application/json');

    req.addEventListener('load', function(){
      if (req.status >= 200 && req.status < 400) {
        res = JSON.parse(req.responseText);

        // clear out current search result table rows
        var prevTableRows = document.getElementsByClassName('searchResultRow');
        while (prevTableRows[0]) {
          prevTableRows[0].remove();
        }

        searchTable = document.getElementById("searchResultTable")
        
        // add appropriate header rows for Franchises table
        header_tr = document.createElement('tr');
        header_tr.setAttribute('class', 'searchResultRow');
        header_elements = ["Franchise", "Developer", "Delete?"];
        for (var i = 0; i < header_elements.length; i++) {
          header_td = document.createElement('th');
        header_td.textContent = header_elements[i]
        header_tr.appendChild(header_td);
        }
        searchTable.appendChild(header_tr);

        // add each row into the search result table
        for (var i = 0; i < res.length; i++) {
          title_tr = document.createElement('tr');
          title_tr.setAttribute('class', 'searchResultRow');
          title_tr.setAttribute('id', res[i][0]);
          
          // name, developer cells
          for (var j = 1; j < 3; j++) {
            td_cell = document.createElement('td');
            td_cell.textContent = res[i][j];
            title_tr.appendChild(td_cell);
          }

          // add delete button
          button_td = document.createElement('td');
          del_button = document.createElement('button');
          del_button.setAttribute('type', 'button');
          del_button.setAttribute('class', 'franchiseDelButton');
          del_button.setAttribute('value', res[i][0]);
          del_button.textContent = "Delete"
          button_td.appendChild(del_button);
          title_tr.appendChild(button_td);

          searchTable.appendChild(title_tr);
        }

        // rebind the new delete buttons to trigger delete query
        bind_delete_buttons();

      } else {
        console.log("Error in network request: " + req.statusText);
    }});

    req.send(JSON.stringify(payload));
  });

  
  bind_delete_buttons();

  // 
  Array.from(document.getElementsByClassName("searchButton")).forEach(function(element) {
    element.addEventListener("click", function(event) {
      document.getElementById("searchResults").style.display = "block"
    })
  });
}

// run this every time the search table is remade to bind newly made buttons
function bind_delete_buttons() {
  Array.from(document.getElementsByClassName("titleDelButton")).forEach(function(element) {
    element.addEventListener("click", function(event) {
      if (confirm('Are you sure you want to delete this from the database?')) {
        // POST with button's value, which is the row's ID (event.target.value)
        var req = new XMLHttpRequest();
        var payload = {"action": "deleteTitle",
                      "ButtonVal": event.target.value
                      };
        req.open('POST', '/delete', true);
        req.setRequestHeader('Content-Type', 'application/json');
        req.send(JSON.stringify(payload));

        // if successful:
        var row = document.getElementById(event.target.value);
        row.parentNode.removeChild(row);
        document.getElementById("delSuccessful").style.display = "block";
          setTimeout(function() {
          document.getElementById("delSuccessful").style.display = "none"
          }, 1500);

        // not successful
        document.getElementById("updateFailed").style.display = "block";
        setTimeout(function() {
          document.getElementById("updateFailed").style.display = "none"
        }, 1500);
      } 
    })
  });
  Array.from(document.getElementsByClassName("devDelButton")).forEach(function(element) {
    element.addEventListener("click", function(event) {
      if (confirm('Are you sure you want to delete this from the database?')) {
        // POST with button's value, which is the row's ID (event.target.value)
        var req = new XMLHttpRequest();
        var payload = {"action": "deleteDev",
                      "ButtonVal": event.target.value
                      };
        req.open('POST', '/delete', true);
        req.setRequestHeader('Content-Type', 'application/json');
        req.send(JSON.stringify(payload));
        // if successful:
        var row = document.getElementById(event.target.value);
        row.parentNode.removeChild(row);        
        document.getElementById("delSuccessful").style.display = "block";
          setTimeout(function() {
          document.getElementById("delSuccessful").style.display = "none"
          }, 1500);


        // not successful
        document.getElementById("updateFailed").style.display = "block";
        setTimeout(function() {
          document.getElementById("updateFailed").style.display = "none"
        }, 1500);
      } 
    })
  });
  Array.from(document.getElementsByClassName("platDelButton")).forEach(function(element) {
    element.addEventListener("click", function(event) {
      if (confirm('Are you sure you want to delete this from the database?')) {
        // POST with button's value, which is the row's ID (event.target.value)
        var req = new XMLHttpRequest();
        var payload = {"action": "deletePlat",
                      "ButtonVal": event.target.value
                      };
        req.open('POST', '/delete', true);
        req.setRequestHeader('Content-Type', 'application/json');
        req.send(JSON.stringify(payload));
        // if successful:
        var row = document.getElementById(event.target.value);
        row.parentNode.removeChild(row);        
        document.getElementById("delSuccessful").style.display = "block";
          setTimeout(function() {
          document.getElementById("delSuccessful").style.display = "none"
          }, 1500);

        // not successful
        document.getElementById("updateFailed").style.display = "block";
        setTimeout(function() {
          document.getElementById("updateFailed").style.display = "none"
        }, 1500);
      } 
    })
  });
  Array.from(document.getElementsByClassName("franchiseDelButton")).forEach(function(element) {
    element.addEventListener("click", function(event) {
      if (confirm('Are you sure you want to delete this from the database?')) {
        // POST with button's value, which is the row's ID (event.target.value)
        var req = new XMLHttpRequest();
        var payload = {"action": "deleteFranchise",
                      "ButtonVal": event.target.value
                      };
        req.open('POST', '/delete', true);
        req.setRequestHeader('Content-Type', 'application/json');
        req.send(JSON.stringify(payload));
        // if successful:
        var row = document.getElementById(event.target.value);
        row.parentNode.removeChild(row);        
        document.getElementById("delSuccessful").style.display = "block";
          setTimeout(function() {
          document.getElementById("delSuccessful").style.display = "none"
          }, 1500);

        // not successful
        document.getElementById("updateFailed").style.display = "block";
        setTimeout(function() {
          document.getElementById("updateFailed").style.display = "none"
        }, 1500);
      } 
    })
  });
}
