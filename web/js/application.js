/**
 * Some globals used throughout the script.
 */
var contentTbl,
    defaultContent = 'tv';

/**
 * Main method that delegates setting up the page.
 */
function setupUI() {
	setupLayout();
	setupTable();
	setupMsgDialog();
	setupUploadDialog();
}

/**
 * Uses the fancy jquery.layout plugin to layout the
 * main sections of the page and handles the media events.
 */
function setupLayout() {
	$('body').layout({
		west__showOverflowOnHover : true,
		resizable : false,
		closable : false
	});

	$('.ui-layout-west a').click(function() {
		var id = $(this).attr('id');
		if (id == 'upload') {
		    $('#uploadForm :input').val('');
			$('#errorBox').html('');
			$('#uploadDialog').dialog('open');
		} else {
			$('.ui-layout-west a').removeClass('selectedCat');
			$(this).addClass('selectedCat');
			getContent(id);
		}
		return false;
	});

    // Select default content
	$(".ui-layout-west a[id='" + defaultContent + "']").addClass('selectedCat');
}

/**
 * Creates & populates the table as well as wiring the table row events.
 */
function setupTable() {

    // Clear out the empty rows
    $('tbody').html('');

	contentTbl = $('#contentTbl').dataTable({
	    bPaginate : true,
	    bLengthChange : false,
		bAutoWidth : false,
		iDisplayLength : 25,
		sPaginationType : 'full_numbers',
		bSortClasses : false,
		bProcessing : true,
		aaSorting : [],
		sAjaxSource : 'json/' + defaultContent + '/',
		fnInitComplete : function() { hideAjaxLoader(); },
		oLanguage: {
				sSearch : 'Search:',
				sZeroRecords : 'No files found',
				sInfo : 'Showing _START_ to _END_ of _TOTAL_ files'
		},
		aoColumns : [
		        { bVisible : false, bSearchable : false },
		        { sTitle : 'Title' },
		        { sTitle : 'Newsgroup' },
		        { sTitle : 'Submitted By' },
		        { sTitle : 'Size' },
		        { sTitle : 'Age' }
			]
	});

	setupRowEvents();

	// Create the ajax loader for table processing
	$('#contentTbl_processing').attr('style', 'visibility:visible;').html('<img src="http://media.birdpiss.com/css/images/ajax-loader.gif" alt="Shovelling coal into the server..." />');

	// Make the search textbox a little longer and add focus
	$('#contentTbl_filter :text:first').addClass('ui-widget input nzbSearch').attr('size', 50).focus();

	// Add a download btn next to search
	$('#contentTbl_filter').append('&nbsp;<input type="button" value="Download Selected" id="downloadBtn" class="ui-widget-content nzbBtn" />');

    // Add an event to our download btn
	$('#downloadBtn').click(function() {
	    var selectedRows = getSelectedRows();
	    if (selectedRows.length > 0) {
    		window.location = 'download/' + selectedRows;
			clearSelectedRows();
    	} else {
    	    $('#msgDialog').dialog('open').html("<span style='color:red;'>Download Fail:</span> Can't give you something you didn't ask for");
    	}
	});
}

/**
 * We use the 'live' methods cause we want to bind the events
 * to the future rows or data.
 */
function setupRowEvents() {

	$('#contentTbl tbody tr').live('mouseover', (function() {
	    if (! $(this).hasClass('selected')) {
	        $(this).addClass('hover');
	    }
	}));

	$('#contentTbl tbody tr').live('mouseout', (function() {
	    if (! $(this).hasClass('selected')) {
	        $(this).removeClass('hover');
	    }
	}));

	$('#contentTbl tbody tr').live('click', (function() {
	    if (! $(this).hasClass('selected')) {
	        $(this).removeClass('hover').addClass('selected');
	    } else {
	        $(this).removeClass('selected');
	    }
	}));
}

/**
 * Returns an slash separated string containing all the selected media ids.
 *
 * @return string - slash separated string of primary keys of the selected content
 */
function getSelectedRows() {
    var selectedRows = '',
        tblRows = contentTbl.fnGetNodes(),
        data,
		numRows = tblRows.length;
    for (var i = 0; i < numRows; i++) {
        if ($(tblRows[i]).hasClass('selected')) {
            data = contentTbl.fnGetData(i);
            selectedRows += data[0] + '/';
		}
    }
    return selectedRows;
}

/**
 * Clears out any selected rows. Called after a download.
 */
function clearSelectedRows() {
    var tblRows = contentTbl.fnGetNodes(),
		tblRow,
		numRows = tblRows.length;
    for (var i = 0; i < numRows; i++) {
		tblRow = $(tblRows[i]);
        if ($(tblRow).hasClass('selected')) {
            $(tblRow).removeClass('selected');
        }
    }
}

/**
 * Setups our download dialogs.
 */
function setupMsgDialog() {
	$('#msgDialog').dialog({
	    autoOpen : false,
	    modal : true,
	    title : 'Message'
	});
}

/**
 * Setups our upload form dialog and it's validator.
 */
function setupUploadDialog() {

    $('#size').numeric({ allow : '.' });

	$('#uploadDialog').dialog({
		modal : true,
		autoOpen : false,
		title : 'Thanks for sharing',
		width : '450px',
		buttons : {
			Upload : function() {
		        $('#uploadForm').submit();
		    }
		}
	});

	$('#uploadForm').validate({
	    errorClass : 'important',
	    errorLabelContainer : '#errorBox',
	    wrapper : 'li',
	    rules : {
	        usenet_file : 'required',
	        title : 'required',
	        media : 'required',
	        size : { required : true, number : true, min : 1 }
	    },
	    messages : {
	        usenet_file : 'File fail',
	        title : 'Title fail',
	        media : 'Media fail',
	        size : { required : 'Size fail', number : 'Size must be a number', min : 'Size is too small' }
	    },
		submitHandler : function(form) {
			$(form).ajaxSubmit({
				dataType : 'json',
				timeout : 12000,
				error : function(XMLHttpRequest, textStatus, errorThrown) {
					$('#msgDialog').dialog('open').html('<span style="color:red;">Upload Fail:</span> ' + errorThrown);
				},
				beforeSubmit : function(formData, jqForm, options) {
	                $('#uploadingMsg').attr('style', 'display:inline;');
				},
				success : function(data) {
					if (data.response == 'success') {
						getContent(defaultContent);
					} else {
						handleFail(data);
					}
				},
				complete : function(XMLHttpRequest, textStatus) {
					$('#uploadDialog').dialog('close');
					$('#uploadingMsg').attr('style', 'display:none;');
				}
			});
		}
	});

	// Wire the 'enter' key to submit the form if hit on the last input elements
	$('#uploadForm :input[class!="formInput"]').keypress(function(e) {
	    if ((e.which && e.which == 13) || (e.keyCode && e.keyCode == 13)) {
	        $('#uploadForm').submit();
	        return false;
	    }
	    return true;
	});
}

/**
 * Calls the server for the selected media content & clears
 * the table data & replaces it with the new media data.
 *
 * @param type - tv, movies, music, software, etc...
 */
function getContent(type) {
    showAjaxLoader();
    clearTable();
	$.getJSON('json/' + type.toLowerCase() + '/', function(data) {
		hideAjaxLoader();
		if (data.response == 'success') {
			contentTbl.fnAddData(data.aaData);
		} else {
			handleFail(data);
		}
	});
}

/**
 * Clears the data in the table and the search field.
 */
function clearTable() {
	contentTbl.fnClearTable();
	$('#contentTbl_filter :text:first').val('');
	contentTbl.fnFilter('');
}

/**
 * Displays our animated ajax loader image.
 */
function showAjaxLoader() {
    $('#contentTbl_processing').attr('style', 'visibility:visible;');
}

/**
 * Hides our animated ajax loader image.
 */
function hideAjaxLoader() {
    $('#contentTbl_processing').attr('style', 'visibility:hidden;');
}

/**
 * Something bad happened so we're gonna redirect the user
 */
function handleFail(data) {
	alert('Failed Response - Code: ' + data.response + ' - Url: ' + data.url);
	window.location = data.url;
}
