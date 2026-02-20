
const help_list = ['Aberdeen', 'St-Albans', 'Birmingham', 'Bath', 'Blackburn','Bradford', 'British-Forces', 'Bournemouth', 'Bolton', 'Brighton',
       'Bromley', 'Bristol', 'Northern-Ireland', 'Carlisle', 'Cambridge','Cardiff', 'Chester', 'Chelmsford', 'Colchester', 'Croydon','Canterbury', 'Coventry', 'Crewe', 'Dartford', 'Dundee', 'Derby',
       'Dumfries-and-Galloway', 'Durham', 'Darlington', 'Doncaster','Dorchester', 'Dudley', 'East-London', 'Central-London','Edinburgh', 'Enfield', 'Exeter', 'Falkirk-and-Stirling',
       'Blackpool', 'Glasgow', 'Gloucester', 'Guildford', 'Harrow','Huddersfield', 'Harrogate', 'Hemel-Hempstead', 'Hereford','OuterHebrides', 'Hull', 'Halifax', 'Ilford', 'Ipswich',
       'Inverness', 'Kilmarnock', 'Kingston-upon-Thames', 'Kirkwall','Kirkcaldy', 'Liverpool', 'Lancaster', 'Llandrindod-Wells','Leicester', 'Llandudno', 'Lincoln', 'Leeds', 'Luton',
       'Manchester', 'Rochester', 'Milton-Keynes', 'Motherwell','North-London', 'Newcastle-upon-Tyne', 'Nottingham', 'Northampton','Newport', 'Norwich', 'North-West-London', 'Oldham', 'Oxford',
       'Paisley', 'Peterborough', 'Perth', 'Plymouth', 'Portsmouth','Preston', 'Reading', 'Redhill', 'Romford', 'Sheffield', 'Swansea','South-East-London', 'Stevenage', 'Stockport', 'Slough', 'Sutton',
       'Swindon', 'Southampton', 'Salisbury', 'Sunderland','Southend-on-Sea', 'Stoke-on-Trent', 'South-West-London','Shrewsbury', 'Taunton', 'Galashiels', 'Telford', 'Tonbridge',
       'Torquay', 'Truro', 'Cleveland', 'Twickenham', 'Southall','West-London', 'Warrington', 'Central-London', 'Watford','Wakefield', 'Wigan', 'Worcester', 'Walsall', 'Wolverhampton','York', 'Lerwick']

const city_list = [];
let return_response;


function input_sanitiser(input_str){
    //removes all non characters from input_str and returns a list of these separated values

    let parsed_str = input_str.replace(/[^a-zA-Z\s-]/g,'');
    let rtn_list = parsed_str.split(" ");
    
    for (let i = 0; i < rtn_list.length;i++){
        if (rtn_list[i] == ''){
            rtn_list.splice(i,1);
            i = -1;
        }
        else{
           rtn_list[i] = rtn_list[i].replace(/-/g," ");
        }
        console.log(rtn_list[i]);
    }

    return rtn_list;
}


function remove_from_city_list(item){
    for (i = 0; i< city_list.length; i++){
        if (`div_${city_list[i]}` == item){
            city_list.splice(i,1);
        }
    }
}


function log_city_list (){
    let sanitised_lst = input_sanitiser(document.getElementById('city_input').value);

    const output_div = document.getElementById('community_output');

    for (i = 0; i < sanitised_lst.length;i++){
        if(city_list.indexOf(sanitised_lst[i]) == -1){
            city_list.push(sanitised_lst[i]);

            const new_div = document.createElement('div')
            new_div.id = `div_${sanitised_lst[i]}`;
            new_div.className = 'input_city';
            new_div.innerHTML = sanitised_lst[i];

            new_div.addEventListener('click',function (ev) {
                document.getElementById(new_div.id).remove();

                //removes the element from the city list too
                remove_from_city_list(new_div.id);
                console.log(city_list);
            })


            output_div.appendChild(new_div);
        }
    }
};


function create_community_div(JSON_response){
    const keys = Object.keys(JSON_response);

    const delete_button = document.createElement('button');
    delete_button.className = 'community_delete';

    const house_div = document.getElementById('test');
    keys.forEach(element => {
        const com_div = document.createElement('div');
        com_div.className = 'community_div';
        com_div.appendChild(create_response_table(JSON_response,element));

        const delete_button = document.createElement('button');
        delete_button.className = 'community_delete';
        delete_button.id = `button_${element}`;

        com_div.appendChild(delete_button);
        house_div.appendChild(com_div);

        document.getElementById(`button_${element}`).addEventListener('click', function(ev){
            const container_div = ev.target.closest('.community_div');

            //remove the elements within the table from the maptile
            
            container_div.remove();
        })
    });

    return house_div;
}

function append_city_pointers(JSON_response){
    const keys = Object.keys(JSON_response);
    
    keys.forEach(element => {
        L.marker([JSON_response[element]['lat'],JSON_response[element]['lon'] ]).addTo(markers);
    })


}


function drag_start_handler(ev){
    //ev.preventDefault();
    console.log(ev.target.textContent);
    ev.dataTransfer.setData('Text',ev.target.id);
}


function drag_over_handler(ev){
    ev.preventDefault();
}


function drop_handler(ev){
    ev.preventDefault();

    console.log(ev.target.id);

    const drop_data = ev.dataTransfer.getData('Text')
    ev.target.closest('Table').appendChild(document.getElementById(drop_data));
}


//Creates a new table for each key of the JSON response
function create_response_table(JSON_response,key){
    const com_table = document.createElement('table');
    com_table.id = String(key);
    

    com_table.addEventListener('drop',function (e){
        drop_handler(e);
    })

    com_table.addEventListener('dragover', function (e){
        drag_over_handler(e);
    })

    const header_row = document.createElement('tr');
    const header = document.createElement('th');
    
    header.textContent = key;
    header_row.appendChild(header);
    com_table.appendChild(header_row);


    JSON_response[key].forEach(element => {
        const row = document.createElement('tr');
        row.id = element;

        const row_data = document.createElement('td');
        row_data.textContent = element;

        row.draggable = true;
        row.addEventListener('dragstart', function (e) {
            drag_start_handler(e);
        })

        row.addEventListener('dragover', function (e){
            drag_over_handler(e);
        })


        row.appendChild(row_data);
        com_table.appendChild(row);
    });

    return com_table
}


var map = L.map('map_div').setView([52.636182, -1.133126], 7);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

var markers = L.layerGroup().addTo(map);

document.getElementById('city_input').addEventListener('keyup',function (event){
    // if event is the enter key, add current value to the city_array 
    if (event.code === 'Enter'){
        log_city_list();
        event.target.value = '';
    }
})


document.getElementById('button').addEventListener('click',function (){
    const request = new XMLHttpRequest();

    request.open('GET',`/louvain?cities_list=${city_list}`);
    request.send();

    request.onload = function() {
        return_response = JSON.parse(request.responseText);

        let div_insert = document.getElementById('test');

        div_insert.innerHTML = '';
        div_insert = create_community_div(return_response['graph']);
        
        //generates pointers on maptile
        markers.clearLayers();
        append_city_pointers(return_response['coordinates']);


    }
})

document.getElementById('help_button').addEventListener('click',function (event){
    const overlay_container = document.getElementById('help_overlay');

    const popup_div = document.createElement('div');

    const popup_p = document.createElement('p');
    popup_p.textContent = "Neat Nav utilises unique post codes for grouping. The locations avaliable are below:"
    popup_div.appendChild(popup_p);

    const popup_table = document.createElement('table');
    
    help_list.forEach(element => {
        const new_row = document.createElement('tr');
        const new_data = document.createElement('td');
        new_data.textContent = element;
    
        new_row.appendChild(new_data);
        popup_table.appendChild(new_row);
    });

    popup_div.appendChild(popup_table);

    popup_div.addEventListener('click',function (){
        popup_div.remove();
        overlay_container.style.display = "none";
    })

    overlay_container.appendChild(popup_div);
    overlay_container.style.display = "inline";

})