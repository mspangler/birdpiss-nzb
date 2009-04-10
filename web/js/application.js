
function setupUI() {
	setupLayout();
	setupTable();
	setupDownloadDialog();
	setupUploadDialog();
}

function setupLayout() {
	$('body').layout({
		west__showOverflowOnHover : true,
		resizable : false,
		closable : false
	});

	$('.ui-layout-west a').click(function() {
		var txt = $(this).text();
		if (txt == 'Upload') {
			$('#uploadDialog').dialog('open');
		} else {
			$('.ui-layout-west a').removeClass('selectedCat');
			$(this).addClass('selectedCat');
			getContent(txt);
		}
		return false;
	});

	$(".ui-layout-west a:contains('Movies')").addClass('selectedCat');
}

function reloadTable(data) {
	if (contentTbl) {
		contentTbl.fnClearTable();
		contentTbl.fnAddData(data.json);
	}
}

var contentTbl;
function setupTable() {

	// Load movies by default
	getContent('movies');

	contentTbl = $('#contentTbl').dataTable({
	    bPaginate : true,
	    bLengthChange : false,
		bAutoWidth : false,
		iDisplayLength : 25,
		sPaginationType : 'full_numbers',
		bSortClasses : false,
		aaSorting : [[]],
		bStateSave : true,
		aaData : data.json,
		oLanguage: {
				sSearch : 'Search:',
				sZeroRecords: 'No files found',
				sInfo: 'Showing _START_ to _END_ of _TOTAL_ files',
				sInfoEmpty: ''
		},
		aoColumns : [
		        { bVisible : false, bSearchable : false },
		        { sTitle : 'Title' },
		        { sTitle : 'Genre' },
		        { sTitle : 'Filename' },
		        { sTitle : 'Rating' },
		        { sTitle : 'Days Active' }
			],
		fnRowCallback : function(nRow, aData, iDisplayIndex) {
			var cssClass = nRow.className;
			nRow.onmouseover = function() {
				if (!$(nRow).hasClass('selected')) {
					nRow.className = 'hover';
				}
			};
			nRow.onmouseout = function() {
				if (!$(nRow).hasClass('selected')) {
					nRow.className = cssClass;
				}
			};
			nRow.onclick = function() {
				if (!$(nRow).hasClass('selected')) {
					nRow.className = 'selected';
				} else {
					nRow.className = cssClass;
				}
			};

			return nRow;
		}
	});

	// Make the search textbox a little longer
	$('#contentTbl_filter :text:first').addClass('ui-widget input nzbSearch').attr('size', 50).focus();

	// Add a download btn next to search
	$('#contentTbl_filter').append('&nbsp;<input type="submit" value="Download Selected" id="downloadBtn" class="ui-widget-content nzbBtn" />');

	$('#downloadBtn').click(function() {
		$('#downloadDialog').dialog('open');
	});
}

function setupDownloadDialog() {
	$('#downloadDialog').dialog({
		modal : true,
		autoOpen : false,
		width : '350px',
		buttons : {
			Close : function() {
				$(this).dialog('close');
			}
		}
	});
}

function setupUploadDialog() {
	$('#uploadDialog').dialog({
		modal : true,
		autoOpen : false,
		width : '400px',
		buttons : {
			Close : function() {
				$(this).dialog('close');
			}
		}
	});
}

function getTestJson(type) {
	var rows = [], title, filename;
	switch (type) {
		case 'Movies':
			title = 'Dog Day Afternoon'
			filename = 'dogDayAfternoon.avi'
			break;
		case 'Music':
			title = 'Rancid'
			filename = 'rancid.mp3'
			break;
		case 'Software':
			title = 'Ubuntu'
			filename = 'ubuntu.tar.gz'
			break;
		default:
			title = 'Unknown';
			filename = 'unknown.txt';
	}
	for (i = 0; i < 125; i++) {
		// Data in index 0 is suppose to represent the id of the content
		rows[i] = [ i, title, type, filename, '*****', 25 + i ];
	}
	return { 'json' : rows };
}

function getContent(type) {
	$.getJSON('controller.url', { type : type.toLowerCase() }, function(data) {
		console.log(data.json);
		reloadTable(data);
	});
}
