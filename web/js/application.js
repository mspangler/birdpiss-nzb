
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
		    $('#uploadForm :input').val('');
			$('#errorBox').html('');
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

var contentTbl;
function setupTable() {

    $('tbody').html('');

	contentTbl = $('#contentTbl').dataTable({
	    bPaginate : true,
	    bLengthChange : false,
		bAutoWidth : false,
		iDisplayLength : 25,
		sPaginationType : 'full_numbers',
		bSortClasses : false,
		aaSorting : [],
		bStateSave : false,
		sAjaxSource : 'server/process.php?type=movies',
		oLanguage: {
				sSearch : 'Search:',
				sZeroRecords: 'No files found',
				sInfo: 'Showing _START_ to _END_ of _TOTAL_ files',
				sInfoEmpty: ''
		},
		aoColumns : [
		        { bVisible : false, bSearchable : false },
		        { sTitle : 'Title' },
		        { sTitle : 'Newsgroup' },
		        { sTitle : 'Submitted By' },
		        { sTitle : 'Size' },
		        { sTitle : 'Age' }
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
				console.log('Content Id: ' + aData[0]);
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
		title : 'Please enjoy this tasty file',
		buttons : {
			Download : function() {
				$(this).dialog('close');
			}
		}
	});
}

function setupUploadDialog() {
    $('#uploadForm :input').val('');
    $('#size').numeric({ allow:'.' });
	$('#uploadDialog').dialog({
		modal : true,
		autoOpen : false,
		title : 'Thanks for sharing',
		width : '450px',
		buttons : {
			Upload : function() {
		        $('#upload').submit();
		    }
		}
	});

	$('#uploadForm').validate({
	    errorClass : 'important',
	    errorLabelContainer : '#errorBox',
	    wrapper : 'li',
	    rules : {
	        upload : 'required',
	        title : 'required',
	        newsgroup : 'required',
	        size : 'required'
	    },
	    messages : {
	        upload : 'You forgot to upload the file',
	        title : 'Please enter a title',
	        newsgroup : 'Please enter a newsgroup',
	        size : 'Please enter the final size of the file'
	    }
	});
}

function getContent(type) {
	$.getJSON('server/process.php', { type : type.toLowerCase() }, function(data) {
		reloadTable(data);
	});
}

function reloadTable(data) {
	if (contentTbl) {
		contentTbl.fnClearTable();
		contentTbl.fnAddData(data.aaData);
	}
}
