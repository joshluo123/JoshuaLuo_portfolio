document.addEventListener("DOMContentLoaded", bindButtons);

function bindButtons() {
  document.getElementById("selTitleSearch").addEventListener("click", function(event){
    document.getElementById("updateDevSearch").style.display = "none";
    document.getElementById("updatePlatSearch").style.display = "none";
    document.getElementById("updateFranchiseSearch").style.display = "none";

    document.getElementById("updateTitleSearch").style.display = "block";

    document.getElementById("updateSuccessful").style.display = "none"
  });

  document.getElementById("selDevSearch").addEventListener("click", function(event){
    document.getElementById("updateTitleSearch").style.display = "none";
    document.getElementById("updatePlatSearch").style.display = "none";
    document.getElementById("updateFranchiseSearch").style.display = "none";

    document.getElementById("updateDevSearch").style.display = "block";

    document.getElementById("updateSuccessful").style.display = "none"
  });

  document.getElementById("selPlatSearch").addEventListener("click", function(event){
    document.getElementById("updateTitleSearch").style.display = "none";
    document.getElementById("updateDevSearch").style.display = "none";
    document.getElementById("updateFranchiseSearch").style.display = "none";

    document.getElementById("updatePlatSearch").style.display = "block";

    document.getElementById("updateSuccessful").style.display = "none"
  });

  document.getElementById("selFranchiseSearch").addEventListener("click", function(event){
    document.getElementById("updateTitleSearch").style.display = "none";
    document.getElementById("updateDevSearch").style.display = "none";
    document.getElementById("updatePlatSearch").style.display = "none";

    document.getElementById("updateFranchiseSearch").style.display = "block";

    document.getElementById("updateSuccessful").style.display = "none"
  });

  document.getElementById("searchTitleButton").addEventListener("click", function(event) {
    document.getElementById("missingTitleInputs").style.display = "none";
    document.getElementById("missingDevInputs").style.display = "none";
    document.getElementById("missingPlatInputs").style.display = "none";
    document.getElementById("missingFranchiseInputs").style.display = "none";

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

    req.open('POST', '/update', true);
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
                            "Franchise", "Developer", "ESRB Rating", "Update/Edit?"];
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

          // update button
          button_td = document.createElement('td');
          update_button = document.createElement('button');
          update_button.setAttribute('type', 'button');
          update_button.setAttribute('class', 'updateTitleButton');
          update_button.textContent = "Update/Edit";
          button_td.appendChild(update_button);

          // save button, has a value of the ID of the title
          save_button = document.createElement('button');
          save_button.setAttribute('type', 'button');
          save_button.setAttribute('class', 'saveTitleButton');
          save_button.setAttribute('value', res[i][0]);
          save_button.textContent = "Save Changes";
          button_td.appendChild(save_button);
          
          title_tr.appendChild(button_td);

          searchTable.appendChild(title_tr);
        }

        // rebind the new update buttons to trigger update query
        bind_updateTitle_buttons();

      } else {
        console.log("Error in network request: " + req.statusText);
    }});

    req.send(JSON.stringify(payload));
  });

  document.getElementById("searchDevButton").addEventListener("click", function(event) {
    document.getElementById("missingTitleInputs").style.display = "none";
    document.getElementById("missingDevInputs").style.display = "none";
    document.getElementById("missingPlatInputs").style.display = "none";
    document.getElementById("missingFranchiseInputs").style.display = "none";

    var req = new XMLHttpRequest();

    var payload = {"action": "searchDev",
                    "devName": document.getElementById('searchDevName').value,
                    "devCountry": document.getElementById('searchDevCountry').value, 
                    "devFromDate": document.getElementById('searchDevFromDate').value, 
                    "devToDate": document.getElementById('searchDevToDate').value};

    req.open('POST', '/update', true);
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
        header_elements = ["Developer Studio", "Country", "Date Founded", "Update/Edit?"];
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
          
          // name, country, date founded cells
          for (var j = 1; j < 4; j++) {
            td_cell = document.createElement('td');
            td_cell.textContent = res[i][j];
            title_tr.appendChild(td_cell);
          }

          // update button
          button_td = document.createElement('td');
          update_button = document.createElement('button');
          update_button.setAttribute('type', 'button');
          update_button.setAttribute('class', 'updateDevButton');
          update_button.textContent = "Update/Edit";
          button_td.appendChild(update_button);
          title_tr.appendChild(button_td);

          // save button, has a value of the ID of the dev
          save_button = document.createElement('button');
          save_button.setAttribute('type', 'button');
          save_button.setAttribute('class', 'saveDevButton');
          save_button.setAttribute('value', res[i][0]);
          save_button.textContent = "Save Changes";
          button_td.appendChild(save_button);

          searchTable.appendChild(title_tr);
        }

        // rebind the new update buttons to trigger update query
        bind_updateDev_buttons();

      } else {
        console.log("Error in network request: " + req.statusText);
    }});

    req.send(JSON.stringify(payload));
  });

  document.getElementById("searchPlatButton").addEventListener("click", function(event) {
    document.getElementById("missingTitleInputs").style.display = "none";
    document.getElementById("missingDevInputs").style.display = "none";
    document.getElementById("missingPlatInputs").style.display = "none";
    document.getElementById("missingFranchiseInputs").style.display = "none";

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

    req.open('POST', '/update', true);
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
        
        header_elements = ["Platform", "Release Date<br/>(North America)", "Developer", "In Prduction", "Update/Edit?"];
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
          
          // name, release, dev cells
          for (var j = 1; j < 4; j++) {
            td_cell = document.createElement('td');
            td_cell.textContent = res[i][j];
            title_tr.appendChild(td_cell);
          }

          // in production cell
          td_cell = document.createElement('td');
          if (res[i][4]) {
            td_cell.textContent = "Y"
          } else {
            td_cell.textContent = "N"
          }
          title_tr.appendChild(td_cell);

          // add update button
          button_td = document.createElement('td');
          update_button = document.createElement('button');
          update_button.setAttribute('type', 'button');
          update_button.setAttribute('class', 'updatePlatButton');
          update_button.textContent = "Update/Edit";
          button_td.appendChild(update_button);
          title_tr.appendChild(button_td);

          // save button, has a value of the ID of the dev
          save_button = document.createElement('button');
          save_button.setAttribute('type', 'button');
          save_button.setAttribute('class', 'savePlatButton');
          save_button.setAttribute('value', res[i][0]);
          save_button.textContent = "Save Changes";
          button_td.appendChild(save_button);

          searchTable.appendChild(title_tr);
        }

        // rebind the new update buttons to trigger update query
        bind_updatePlat_buttons();

      } else {
        console.log("Error in network request: " + req.statusText);
    }});

    req.send(JSON.stringify(payload));
  });

  document.getElementById("searchFranchiseButton").addEventListener("click", function(event) {
    document.getElementById("missingTitleInputs").style.display = "none";
    document.getElementById("missingDevInputs").style.display = "none";
    document.getElementById("missingPlatInputs").style.display = "none";
    document.getElementById("missingFranchiseInputs").style.display = "none";

    var req = new XMLHttpRequest();

    var payload = {"action": "searchFranchise",
            "franchiseName": document.getElementById('searchFranchiseName').value,
            "franchiseDev": document.getElementById('searchFranchiseDev').value};

    req.open('POST', '/update', true);
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
        header_elements = ["Franchise", "Developer", "Update/Edit?"];
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
          
          // name, developer cells
          for (var j = 1; j < 3; j++) {
            td_cell = document.createElement('td');
            td_cell.textContent = res[i][j];
            title_tr.appendChild(td_cell);
          }

          // add update button
          button_td = document.createElement('td');
          update_button = document.createElement('button');
          update_button.setAttribute('type', 'button');
          update_button.setAttribute('class', 'updateFranchiseButton');
          update_button.textContent = "Update/Edit"
          button_td.appendChild(update_button);
          title_tr.appendChild(button_td);

          // save button, has a value of the ID of the dev
          save_button = document.createElement('button');
          save_button.setAttribute('type', 'button');
          save_button.setAttribute('class', 'saveFranchiseButton');
          save_button.setAttribute('value', res[i][0]);
          save_button.textContent = "Save Changes";
          button_td.appendChild(save_button);

          searchTable.appendChild(title_tr);
        }

        // rebind the new update buttons to trigger update query
        bind_updateFranchise_buttons();

      } else {
        console.log("Error in network request: " + req.statusText);
    }});

    req.send(JSON.stringify(payload));
  });
  
  Array.from(document.getElementsByClassName("searchButton")).forEach(function(element) {
    element.addEventListener("click", function(event) {
      document.getElementById("searchResults").style.display = "block";
    })
  });
}

// run this every time a Title search is made
function bind_updateTitle_buttons() {
  // clicking update/edit buttons make cells editable and show the "Save Changes" button instead
  Array.from(document.getElementsByClassName("updateTitleButton")).forEach(function(element) {
    element.addEventListener("click", function(event) {
      // get list of platforms, franchises, and devs to fill drop down manus
      var req = new XMLHttpRequest();
      payload = {"action": "updateTitleElements"};
      req.open('POST', '/update', true);
      req.setRequestHeader('Content-Type', 'application/json');

      req.addEventListener('load', function(){
        if (req.status >= 200 && req.status < 400) {
          // res["Plats", "Franchises", "Devs"] -> list of each
          res = JSON.parse(req.responseText);

          // change displayed button to Save Changes
          event.target.style.display = "none";
          event.target.nextElementSibling.style.display = "inline";

          // make the row's attributes editable
          var row_element = event.target.parentNode.parentNode;
          var cell_elements = row_element.childNodes;

          // name text input
          var td_cell = document.createElement('td');
          var update_name = document.createElement('input');
          update_name.setAttribute("type", "text");
          update_name.setAttribute("value", cell_elements[0].textContent);
          td_cell.appendChild(update_name);
          row_element.replaceChild(td_cell, cell_elements[0]);

          // platform list options
          var plat_elements = res["Plats"];
          td_cell = document.createElement('td');
          td_cell.style.textAlign = "left";
          var plat_option = document.createElement("input");
          plat_option.setAttribute("type", "checkbox");
          plat_option.setAttribute("value", plat_elements[0][0]);
          td_cell.appendChild(plat_option);
          var plat_name = document.createElement("span");
          plat_name.textContent = plat_elements[0][1];
          td_cell.appendChild(plat_name);
          for (var i = 1; i < plat_elements.length; i++) {
            var break_tag = document.createElement("br");
            td_cell.appendChild(break_tag);

            plat_option = document.createElement("input");
            plat_option.setAttribute("type", "checkbox");
            plat_option.setAttribute("value", plat_elements[i][0]);
            td_cell.appendChild(plat_option);

            plat_name = document.createElement("span");
            plat_name.textContent = plat_elements[i][1];
            td_cell.appendChild(plat_name);
          }
            // set default selections to original values
          var curr_plats = cell_elements[1].childNodes[0].childNodes;
          for (var i = 0; i < curr_plats.length; i ++) {
            var index = 1;
            while (curr_plats[i].textContent != td_cell.childNodes[index].textContent) {
              index += 3;
            }
            td_cell.childNodes[index - 1].setAttribute("checked", true);
          }

          row_element.replaceChild(td_cell, cell_elements[1]);

          // release date selection
          td_cell = document.createElement('td');
          var update_date = document.createElement('input');
          update_date.setAttribute("type", "date");
          update_date.defaultValue = cell_elements[2].textContent;
          td_cell.appendChild(update_date);
          row_element.replaceChild(td_cell, cell_elements[2]);

          // genre options
          var genre_elements = ["Action", "Action-Adventure", "Adventure", "Battle Royale", "Fighting", "First-Person Shooter",
                                "Massively Multiplayer Online Games", "Multiplayer Online Battle Arena", "Platformer", "Racing",
                                "Real-Time Strategy", "Role-Playing Games", "Sandbox/Open World", "Simulation", "Sports",
                                "Strategy", "Survival", "Third-Person Shooter", "Other"];
          td_cell = document.createElement('td');
          var update_genre = document.createElement('select');
          var genre_option = document.createElement('option');
          update_genre.appendChild(genre_option);
          for (var i = 0; i < genre_elements.length; i++) {
            genre_option = document.createElement('option');
            genre_option.setAttribute("value", genre_elements[i]);
            genre_option.textContent = genre_elements[i];
            update_genre.appendChild(genre_option);
          }
          td_cell.appendChild(update_genre);
            // set default selection to original value
          if (cell_elements[3].textContent != "") {
            var index = 1;
            while (cell_elements[3].textContent != update_genre.childNodes[index].textContent) {
              index++;
            }
            update_genre.childNodes[index].selected = true;
          }
          row_element.replaceChild(td_cell, cell_elements[3]);

          // franchise options
          var franchise_elements = res["Franchises"];
          td_cell = document.createElement('td');
          var update_franchise = document.createElement('select');
          var franchise_option = document.createElement('option');
          update_franchise.appendChild(franchise_option);
          for (var i = 0; i < franchise_elements.length; i++) {
            franchise_option = document.createElement('option');
            franchise_option.setAttribute("value", franchise_elements[i][0]);
            franchise_option.textContent = franchise_elements[i][1];
            update_franchise.appendChild(franchise_option);
          }
          td_cell.appendChild(update_franchise);
            // set default selection to original value
          if (cell_elements[4].textContent != "") {
            var index = 1;
            while (cell_elements[4].textContent != update_franchise.childNodes[index].textContent) {
              index++;
            }
            update_franchise.childNodes[index].selected = true;
          }
          row_element.replaceChild(td_cell, cell_elements[4]);

          // developer options
          var dev_elements = res["Devs"];
          td_cell = document.createElement('td');
          var update_dev = document.createElement('select');
          for (var i = 0; i < dev_elements.length; i++) {
            var dev_option = document.createElement('option');
            dev_option.setAttribute("value", dev_elements[i][0]);
            dev_option.textContent = dev_elements[i][1];
            update_dev.appendChild(dev_option);
          }
          td_cell.appendChild(update_dev);
            // set default selection to original value
          var index = 0;
          while (cell_elements[5].textContent != update_dev.childNodes[index].textContent) {
            index++;
            update_dev.childNodes[index].selected = true;
          }
          row_element.replaceChild(td_cell, cell_elements[5]);

          // ESRB options
          var esrb_values = ["E", "T", "M"];
          var esrb_texts = ["E - Everyone", "T - Teen", "M - Mature"];
          td_cell = document.createElement('td');
          var update_esrb = document.createElement('select');
          var esrb_option = document.createElement('option');
          update_esrb.appendChild(esrb_option);
          for (var i = 0; i < esrb_values.length; i++) {
            esrb_option = document.createElement('option');
            esrb_option.setAttribute("value", esrb_values[i]);
            esrb_option.textContent = esrb_texts[i];
            update_esrb.appendChild(esrb_option);
          }
          td_cell.appendChild(update_esrb);
            // set default selection to original value
          if (cell_elements[6].textContent != "") {
            var index = 1;
            while (cell_elements[6].textContent != update_esrb.childNodes[index].value) {
              index++;
            }
            update_esrb.childNodes[index].selected = true;
          }
          row_element.replaceChild(td_cell, cell_elements[6]);
        } else {
        console.log("Error in network request: " + req.statusText);
        }
      });
      req.send(JSON.stringify(payload));
    });
  });

  // executes UPDATE query with inputs
  Array.from(document.getElementsByClassName("saveTitleButton")).forEach(function(element) {
    element.addEventListener("click", function(event) {
      // validate at least one platform is checked and a date is selected
      var title_attributes = event.target.parentNode.parentNode.childNodes

      // make a list of all checked platforms
      var plat_list = [];
      var plat_name = [];
      for (var i = 0; i < title_attributes[1].childNodes.length; i += 3) {
        if (title_attributes[1].childNodes[i].checked) {
          plat_list.push(title_attributes[1].childNodes[i].value);
          plat_name.push(title_attributes[1].childNodes[i + 1].textContent);
        }
      }

      if (title_attributes[0].firstChild.value.trim() == "" || plat_list.length == 0 || title_attributes[2].firstChild.value == "") {
        // displayed required field message
        document.getElementById("missingTitleInputs").style.display = "block";

      } else {
        document.getElementById("missingTitleInputs").style.display = "none";

        var req = new XMLHttpRequest();

        // get input values
        var titleID = event.target.value

        var payload = {"action": "updateTitle",
                        "titleID": titleID,
                        "titleName": title_attributes[0].firstChild.value,
                        "titlePlats": plat_list,
                        "titleRelease": title_attributes[2].firstChild.value,
                        "titleGenre": title_attributes[3].firstChild.value,
                        "titleFranchiseID": title_attributes[4].firstChild.value,
                        "titleDevID": title_attributes[5].firstChild.value,
                        "titleESRB": title_attributes[6].firstChild.value};

        req.open('POST', '/update', true);
        req.setRequestHeader('Content-Type', 'application/json');

        req.addEventListener('load', function(){
          if (req.status >= 200 && req.status < 400) {
            res = JSON.parse(req.responseText);
            
            // successful UPDATE
            if (res["result"]) {
              // change displayed button to Update/Edit
              event.target.style.display = "none";
              event.target.previousElementSibling.style.display = "inline";

              // make the cells not editable, displaying updated values
              var row_element = event.target.parentNode.parentNode;
              var cell_elements = row_element.childNodes;
              
              // updated title name
              var td_cell = document.createElement('td');
              td_cell.textContent = payload["titleName"];
              row_element.replaceChild(td_cell, cell_elements[0]);

              // updated platform list
              td_cell = document.createElement('td');
              var plat_list_tag = document.createElement('ul');
              plat_list_tag.setAttribute("class", "platformList");
              for (var i = 0; i < plat_name.length; i++) {
                list_item = document.createElement('li');
                list_item.textContent = plat_name[i];
                plat_list_tag.appendChild(list_item);
              }
              td_cell.appendChild(plat_list_tag);
              row_element.replaceChild(td_cell, cell_elements[1]);

              // updated release date
              td_cell = document.createElement('td');
              td_cell.textContent = payload["titleRelease"];
              row_element.replaceChild(td_cell, cell_elements[2]);

              // updated genre
              td_cell = document.createElement('td');
              td_cell.textContent = payload["titleGenre"];
              row_element.replaceChild(td_cell, cell_elements[3]);

              // updated franchise
              td_cell = document.createElement('td');
              var franchise_items = title_attributes[4].firstChild.childNodes;
              var index = 0;
              while (title_attributes[4].firstChild.value != franchise_items[index].value) {
                index++;
              }
              td_cell.textContent = franchise_items[index].textContent;
              row_element.replaceChild(td_cell, cell_elements[4]);

              // updated dev
              td_cell = document.createElement('td');
              var dev_items = title_attributes[5].firstChild.childNodes;
              var index = 0;
              while (title_attributes[5].firstChild.value != dev_items[index].value) {
                index++;
              }
              td_cell.textContent = dev_items[index].textContent;
              row_element.replaceChild(td_cell, cell_elements[5]);

              // updated ESRB
              td_cell = document.createElement('td');
              td_cell.textContent = title_attributes[6].firstChild.value;
              row_element.replaceChild(td_cell, cell_elements[6]);

              // show update successful message
              document.getElementById("updateSuccessful").style.display = "block";
              setTimeout(function() {
                document.getElementById("updateSuccessful").style.display = "none";
              }, 1500);
            
            // failed update
            } else {
              document.getElementById("updateFailed").style.display = "block";
              setTimeout(function() {
                document.getElementById("updateFailed").style.display = "none";
              }, 1500);
            }
          } else {
              console.log("Error in network request: " + req.statusText);
          }
        });
        req.send(JSON.stringify(payload));
      }
    });
  });
}

// run this every time a Deveveloper search is made
function bind_updateDev_buttons() {
  Array.from(document.getElementsByClassName("updateDevButton")).forEach(function(element) {
    element.addEventListener("click", function(event) {
        // change displayed button to Save Changes
        event.target.style.display = "none";
        event.target.nextElementSibling.style.display = "inline";

        // make the row's attributes edit-able
        var row_element = event.target.parentNode.parentNode;
        var cell_elements = row_element.childNodes;

        // name text input
        var td_cell = document.createElement('td');
        var update_name = document.createElement('input');
        update_name.setAttribute("type", "text");
        update_name.setAttribute("value", row_element.childNodes[0].textContent);
        td_cell.appendChild(update_name);
        row_element.replaceChild(td_cell, cell_elements[0]);

        // country input
        country_elements = ["Australia", "Canada", "China", "Finland", "France", "German", "Italy",
                            "Japan", "Netherlands", "Poland", "Russia", "South Korea", "Spain",
                            "Sweden", "UK", "USA", "Other"];
        td_cell = document.createElement('td');
        var update_country = document.createElement('select');
        for (var i = 0; i < country_elements.length; i++) {
          var country_option = document.createElement('option');
          country_option.setAttribute("value", country_elements[i]);
          country_option.textContent = country_elements[i];
          update_country.appendChild(country_option);
        }
        td_cell.appendChild(update_country);
          // set default selection to original value
        var index = 0;
        while (cell_elements[1].textContent != update_country.childNodes[index].value) {
          index++;
        }
        update_country.childNodes[index].selected = true;
        row_element.replaceChild(td_cell, cell_elements[1]);

        // date founded selection
        td_cell = document.createElement('td');
        var update_date = document.createElement('input');
        update_date.setAttribute("type", "date");
        update_date.defaultValue = cell_elements[2].textContent;
        td_cell.appendChild(update_date);
        row_element.replaceChild(td_cell, cell_elements[2]);
    });
  });

  // executes UPDATE query with inputs
  Array.from(document.getElementsByClassName("saveDevButton")).forEach(function(element) {
    element.addEventListener("click", function(event) {
      // get input values
      var devID = event.target.value
      var dev_attributes = event.target.parentNode.parentNode.childNodes

      // validate required inputs
      if (dev_attributes[0].firstChild.value.trim() == "" || dev_attributes[2].firstChild.value == "") {
        // displayed required field message
        document.getElementById("missingDevInputs").style.display = "block";

      } else {
        document.getElementById("missingDevInputs").style.display = "none";

        var req = new XMLHttpRequest();

        var payload = {"action": "updateDev",
                        "devID": devID,
                        "devName": dev_attributes[0].firstChild.value,
                        "devCountry": dev_attributes[1].firstChild.value,
                        "devDate": dev_attributes[2].firstChild.value}

        req.open('POST', '/update', true);
        req.setRequestHeader('Content-Type', 'application/json');

        req.addEventListener('load', function(){
          if (req.status >= 200 && req.status < 400) {
            res = JSON.parse(req.responseText);

            if (res["result"]) {
              // change displayed button to Update/Edit
              event.target.style.display = "none";
              event.target.previousElementSibling.style.display = "inline";

              // make the cells not editable, displaying updated values
              var row_element = event.target.parentNode.parentNode;
              var cell_elements = row_element.childNodes;

              // updated dev name
              var td_cell = document.createElement('td');
              td_cell.textContent = payload["devName"];
              row_element.replaceChild(td_cell, cell_elements[0]);

              // updated country
              var td_cell = document.createElement('td');
              td_cell.textContent = payload["devCountry"];
              row_element.replaceChild(td_cell, cell_elements[1]);

              // updated founding date
              var td_cell = document.createElement('td');
              td_cell.textContent = payload["devDate"];
              row_element.replaceChild(td_cell, cell_elements[2]);

              // show update successful message
              document.getElementById("updateSuccessful").style.display = "block";
              setTimeout(function() {
                document.getElementById("updateSuccessful").style.display = "none";
              }, 1500);
            } else {
              // show update failed message
              document.getElementById("updateFailed").style.display = "block";
              setTimeout(function() {
                document.getElementById("updateFailed").style.display = "none";
              }, 1500);
            }
          } else {
              console.log("Error in network request: " + req.statusText);
          }
        });
        req.send(JSON.stringify(payload));
      }
    });
  });
}

// run this every time a Platform search is made
function bind_updatePlat_buttons() {
  Array.from(document.getElementsByClassName("updatePlatButton")).forEach(function(element) {
    element.addEventListener("click", function(event) {
        // change displayed button to Save Changes
        event.target.style.display = "none";
        event.target.nextElementSibling.style.display = "inline";

        // make the row's attributes edit-able
        var row_element = event.target.parentNode.parentNode;
        var cell_elements = row_element.childNodes;

        // name text input
        var td_cell = document.createElement('td');
        var update_name = document.createElement('input');
        update_name.setAttribute("type", "text");
        update_name.setAttribute("value", row_element.childNodes[0].textContent);
        td_cell.appendChild(update_name);
        row_element.replaceChild(td_cell, cell_elements[0]);

        // release date selection
        td_cell = document.createElement('td');
        var update_date = document.createElement('input');
        update_date.setAttribute("type", "date");
        update_date.defaultValue = cell_elements[1].textContent;
        td_cell.appendChild(update_date);
        row_element.replaceChild(td_cell, cell_elements[1]);

        // developer input
        dev_elements = ["Apple", "Atari", "Google", "Microsoft", "Nintendo", "Sega", "Sony"];
        td_cell = document.createElement('td');
        var update_dev = document.createElement('select');
        for (var i = 0; i < dev_elements.length; i++) {
          var dev_option = document.createElement('option');
          dev_option.setAttribute("value", dev_elements[i]);
          dev_option.textContent = dev_elements[i];
          update_dev.appendChild(dev_option);
        }
        td_cell.appendChild(update_dev);
          // set default selection to original value
        var index = 0;
        while (cell_elements[2].textContent != update_dev.childNodes[index].value) {
          index++;
        }
        update_dev.childNodes[index].selected = true;
        row_element.replaceChild(td_cell, cell_elements[2]);

        // in production input
        inProd_elements = ["Y", "N"];
        td_cell = document.createElement('td');
        var update_inProd = document.createElement('select');
        for (var i = 0; i < inProd_elements.length; i++) {
          var inProd_option = document.createElement('option');
          inProd_option.setAttribute("value", inProd_elements[i]);
          inProd_option.textContent = inProd_elements[i];
          update_inProd.appendChild(inProd_option);
        }
        td_cell.appendChild(update_inProd);
          // set default selection to original value
        var index = 0;
        while (cell_elements[3].textContent != update_inProd.childNodes[index].textContent) {
          index++;
        }
        update_inProd.childNodes[index].selected = true;
        row_element.replaceChild(td_cell, cell_elements[3]);
    });
  });

  // executes UPDATE query with inputs
  Array.from(document.getElementsByClassName("savePlatButton")).forEach(function(element) {
    element.addEventListener("click", function(event) {
      // get input values
      var platID = event.target.value
      var plat_attributes = event.target.parentNode.parentNode.childNodes

      // validate required inputs
      if (plat_attributes[0].firstChild.value.trim() == "" || plat_attributes[1].firstChild.value == "") {
        // displayed required field message
        document.getElementById("missingPlatInputs").style.display = "block";

      } else {
        document.getElementById("missingPlatInputs").style.display = "none";

        var req = new XMLHttpRequest();

        var inProd_val;
        if (plat_attributes[3].firstChild.value == "Y") {
          inProd_val = 1;
        } else {
          inProd_val = 0;
        }

        var payload = {"action": "updatePlat",
                        "platID": platID,
                        "platName": plat_attributes[0].firstChild.value,
                        "platDate": plat_attributes[1].firstChild.value,
                        "platDev": plat_attributes[2].firstChild.value,
                        "platInProd": inProd_val}

        req.open('POST', '/update', true);
        req.setRequestHeader('Content-Type', 'application/json');

        req.addEventListener('load', function(){
          if (req.status >= 200 && req.status < 400) {
            res = JSON.parse(req.responseText);

            if (res["result"]) {
              // change displayed button to Update/Edit
              event.target.style.display = "none";
              event.target.previousElementSibling.style.display = "inline";

              // make the cells not editable, displaying updated values
              var row_element = event.target.parentNode.parentNode;
              var cell_elements = row_element.childNodes;

              // updated platform name
              var td_cell = document.createElement('td');
              td_cell.textContent = payload["platName"];
              row_element.replaceChild(td_cell, cell_elements[0]);

              // updated platform release date
              var td_cell = document.createElement('td');
              td_cell.textContent = payload["platDate"];
              row_element.replaceChild(td_cell, cell_elements[1]);

              // update platform dev
              var td_cell = document.createElement('td');
              td_cell.textContent = payload["platDev"];
              row_element.replaceChild(td_cell, cell_elements[2]);

              // update platform in production
              var td_cell = document.createElement('td');
              td_cell.textContent = plat_attributes[3].firstChild.value;
              row_element.replaceChild(td_cell, cell_elements[3]);

              // show update successful message
              document.getElementById("updateSuccessful").style.display = "block";
              setTimeout(function() {
                document.getElementById("updateSuccessful").style.display = "none";
              }, 1500);
            } else {
              // show update failed message
              document.getElementById("updateFailed").style.display = "block";
              setTimeout(function() {
                document.getElementById("updateFailed").style.display = "none";
              }, 1500);
            }
          } else {
            console.log("Error in network request: " + req.statusText);
          }
        });
        req.send(JSON.stringify(payload));
      }
    });
  });
}

// run this every time a Franchise search is made
function bind_updateFranchise_buttons() {
  Array.from(document.getElementsByClassName("updateFranchiseButton")).forEach(function(element) {
    element.addEventListener("click", function(event) {
        // get list of  devs
        var req = new XMLHttpRequest();
        payload = {"action": "updateFranchiseElements"};
        req.open('POST', '/update', true);
        req.setRequestHeader('Content-Type', 'application/json');

        req.addEventListener('load', function(){
          if (req.status >= 200 && req.status < 400) {
            res = JSON.parse(req.responseText);

            // change displayed button to Save Changes
            event.target.style.display = "none";
            event.target.nextElementSibling.style.display = "inline";

            // make the row's attributes edit-able
            var row_element = event.target.parentNode.parentNode;
            var cell_elements = row_element.childNodes;

            // name text input
            var td_cell = document.createElement('td');
            var update_name = document.createElement('input');
            update_name.setAttribute("type", "text");
            update_name.setAttribute("value", row_element.childNodes[0].textContent);
            td_cell.appendChild(update_name);
            row_element.replaceChild(td_cell, cell_elements[0]);

            // developer input
            var dev_elements = res["Devs"];
            td_cell = document.createElement('td');
            var update_dev = document.createElement('select');
            for (var i = 0; i < dev_elements.length; i++) {
              var dev_option = document.createElement('option');
              dev_option.textContent = dev_elements[i][0];
              update_dev.appendChild(dev_option);
            }
            td_cell.appendChild(update_dev);
              // set default selection to original value
            var index = 0;
            while (cell_elements[1].textContent != update_dev.childNodes[index].textContent) {
              index++;
            }
            update_dev.childNodes[index].selected = true;

            row_element.replaceChild(td_cell, cell_elements[1]);

          } else {
              console.log("Error in network request: " + req.statusText);
          }
        });
        req.send(JSON.stringify(payload));
    });
  });

  // executes UPDATE query with inputs
  Array.from(document.getElementsByClassName("saveFranchiseButton")).forEach(function(element) {
    element.addEventListener("click", function(event) {
      // get input values
      var franchiseID = event.target.value
      var franchise_attributes = event.target.parentNode.parentNode.childNodes

      // validate required inputs
      if (franchise_attributes[0].firstChild.value.trim() == "") {
        // displayed required field message
        document.getElementById("missingFranchiseInputs").style.display = "block";

      } else {
        document.getElementById("missingFranchiseInputs").style.display = "none";

        var req = new XMLHttpRequest();

        var payload = {"action": "updateFranchise",
                        "franchiseID": franchiseID,
                        "franchiseName": franchise_attributes[0].firstChild.value,
                        "franchiseDev": franchise_attributes[1].firstChild.value}

        req.open('POST', '/update', true);
        req.setRequestHeader('Content-Type', 'application/json');

        req.addEventListener('load', function(){
          if (req.status >= 200 && req.status < 400) {
            res = JSON.parse(req.responseText);

            if (res["result"]) {
              // change displayed button to Update/Edit
              event.target.style.display = "none";
              event.target.previousElementSibling.style.display = "inline";

              // make the cells not editable, displaying updated values
              var row_element = event.target.parentNode.parentNode;
              var cell_elements = row_element.childNodes;

              // updated franchise name
              var td_cell = document.createElement('td');
              td_cell.textContent = payload["franchiseName"];
              row_element.replaceChild(td_cell, cell_elements[0]);

              // updated franchise developer
              var td_cell = document.createElement('td');
              td_cell.textContent = payload["franchiseDev"];
              row_element.replaceChild(td_cell, cell_elements[1]);

              // show update successful message
              document.getElementById("updateSuccessful").style.display = "block";
              setTimeout(function() {
                document.getElementById("updateSuccessful").style.display = "none";
              }, 1500);
            } else {
              // show update failed message
              document.getElementById("updateFailed").style.display = "block";
              setTimeout(function() {
                document.getElementById("updateFailed").style.display = "none";
              }, 1500);
            }
          } else {
            console.log("Error in network request: " + req.statusText);
          }
        });
        req.send(JSON.stringify(payload));
      }
    });
  });
}