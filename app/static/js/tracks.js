function createTb(server) {

    $("#jsGrid").jsGrid({
        width: "100%",
        height: "550px",
        heading: true,
        paging: true,
        pageSize: 20,
        pagePrevText: "назад",
        pageNextText: "вперед",
        pageFirstText: "начало",
        pageLastText: "конец",
        pagerFormat: "Страницы: {first} {prev} {pages} {next} {last}    {pageIndex} из {pageCount}",
        pageNavigatorNextText: "...",
        pageNavigatorPrevText: "...",
        filtering: true,

        controller: {
            loadData: function(filter) {
                console.log(filter, 1);
                filter.Name = (filter.Name === undefined || filter.Name === null) ? "" : filter.Name;
                console.log(filter, 2);
                const result = dataServer.filter(function (el) {
                    return el.Name.includes(filter.Name)
                });
                return result;
            },
            updateItem: function(item) {
                item.rowid = item.CustomerId;
                return $.ajax({
                    type: "PUT",
                    url: "/crud/chinook/tracks",
                    data: item,
                });
            },
            insertItem: function(item) {
                item.rowid = item.CustomerId;
                return $.ajax({
                    type: "POST",
                    url: "/crud/chinook/tracks",
                    data: item,
                });
            },
           deleteItem: function(item) {
            item.rowid = item.CustomerId;
                $.ajax({
                    type: "DELETE",
                    url: "/crud/chinook/tracks",
                    data: item
                });
            },

        },
        data : server,
        fields: [
            { name: "rowid", type: "number", width: 40, visible:false},
            { name: "Name", type: "textarea", width: 100},
            { name: "AlbumId", title:"AId", filtering:false,type: "number", width: 50},
            { name: "GenreId",title:"GId", filtering:false, type: "number", width: 30},
            { name: "Composer",type: "text", width: 90, filtering:false,visible:true},
            { name: "Milliseconds", title:"MSeconds", filtering:false, type: "number", width: 70},
            { name: "UnitPrice", title:"Price", filtering:false,type: "number", width: 40 },
        ]
    });
}

var dataServer = null;

$.ajax({
    url: "/crud/chinook/tracks?method=get_rows",
    dataType: "json",
  }).done(function(data){
      dataServer = data;
      createTb(data);
  })