function createTb(server) {

    $("#jsGrid").jsGrid({
        width: "100%",
        height: "550px",
        heading: true,
        inserting: true,
        editing: true,
        sorting: true,
        paging: true,
        filtering: false,

        pagePrevText: "назад",
        pageNextText: "вперед",
        pageFirstText: "начало",
        pageLastText: "конец",
        pagerFormat: "Страницы: {first} {prev} {pages} {next} {last}    {pageIndex} из {pageCount}",
        pageNavigatorNextText: "...",
        pageNavigatorPrevText: "...",
        deleteConfirm: "Удаление! Вы уверенны?",

        controller: {
            loadData: function(filter) {
                // const result = dataServer.filter(function (el) {
                //     return el.ContactName.includes(filter.ContactName);
                // });
                // return result;
            },
            updateItem: function(item) {
                item.rowid = item.CustomerId;
                return $.ajax({
                    type: "PUT",
                    url: "/crud/chinook/Customers",
                    data: item,
                });
            },
            insertItem: function(item) {
                item.rowid = item.CustomerId;
                return $.ajax({
                    type: "POST",
                    url: "/crud/chinook/Customers",
                    data: item,
                });
            },
           deleteItem: function(item) {
            item.rowid = item.CustomerId;
                $.ajax({
                    type: "DELETE",
                    url: "/crud/chinook/Customers",
                    data: item
                });
            },

        },
        data : server,
        fields: [
            { name: "rowid", type: "number", width: 40, visible:false},
            { name: "CustomerId", title:"id", type: "text", width: 35, editing: false, inserting: false},
            { name: "FirstName", type: "textarea", width: 50, },
            { name: "LastName", type: "text", width: 70, },
            { name: "Company", type: "text", width: 80, visible:false},
            { name: "Address", type: "text", width: 80},
            { name: "City", type: "text", width: 80 },
            { name: "State", type: "text", width: 30 },
            { name: "Country", type: "text", width: 40 },
            { name: "PostalCode", type: "text", width: 60 },
            { name: "Phone", type: "text", width: 60 },
            { name: "Fax", type: "text", width: 60, visible:false},
            { name: "Email", type: "text", width: 60 , visible:true},
            { name: "SupportRepId", title : "SPI", type: "text", width: 30},
            {
                type: "control",
            }
        ]
    });
}

var dataServer = null;

$.ajax({
    url: "/crud/chinook/Customers?method=get_rows",
    dataType: "json",
  }).done(function(data){
      dataServer = data;
      createTb(data);
  })