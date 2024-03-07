function closeModal() {
    $('#education-modal').hide();
    $('#edit-education-modal').hide();
    $('#plField-modal').hide();
    $('#edit-plField-modal').hide();
    $('#paField-modal').hide();
    $('#edit-paField-modal').hide();
    $('#publicationField-modal').hide();
    $('#edit-publicationField-modal').hide();
    $('#aopField-modal').hide();
    $('#edit-aopField-modal').hide();
    $('#admissionField-modal').hide();
    $('#edit-admissionField-modal').hide();
    $('#membershipField-modal').hide();
    $('#edit-membershipField-modal').hide();
}

function showLicense(edit) {
    if (edit === 'edit') {$('#edit-plField-modal').show();}
    else {$('#plField-modal').show();}
    document.getElementById('pl-title').value = '';
    document.getElementById('pl-title').focus();
}
function addLicense() {
    const titleInput = document.getElementById('pl-title');
    const licenseList = document.getElementById('pl-list');

    // Collect data to send asynchronously
    const server_data = [
        {attorneyId: '{{ current_attorney.id }}'},
        {title: titleInput.value}
    ];
    // Send data
    $.ajax({
       type: 'POST',
       url: "/add_license",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function(results) {
           console.log(results);
           var licenseId = results['licenseId'];
           // Add the new license to the list
           const newLicense = document.createElement('li');
           newLicense.classList.add('list-entry');
           newLicense.id = 'licenseId' + licenseId;     // unique id needed for delete functionality
           licenseList.appendChild(newLicense);
           const divBullet = document.createElement('div');
           divBullet.classList.add('bullet');
           divBullet.appendChild(document.createTextNode(titleInput.value));
           newLicense.appendChild(divBullet);
           const buttonDiv = document.createElement('div');
           const editA = document.createElement('a');
           // editA.onclick =
           editA.appendChild(document.createTextNode('Edit'));
           editA.href = '#';
           editA.classList.add('button');
           buttonDiv.appendChild(editA);
           const deleteA = document.createElement('a');
           deleteA.onclick = function() { deleteLicense(licenseId); };
           deleteA.appendChild(document.createTextNode('Delete'));
           deleteA.href = '#';
           deleteA.classList.add('button');
           buttonDiv.appendChild(deleteA);
           newLicense.appendChild(buttonDiv);
       }
     });
    closeModal();
}
function editLicense(id){
    const server_data = [
        {id: id},
        {newTitle: document.getElementById('pl-title-edit').value}
    ];
    $.ajax({
       type: "POST",
       url: "/edit_license",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function(result) {
         console.log(result);
       }
     });
    closeModal();
}
function deleteLicense(licenseId){
    const server_data = [
        {licenseId: licenseId}
    ];
    console.log(server_data);
    $.ajax({
       type: "POST",
       url: "/delete_license",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function() {
         console.log('deleted license');
         const listEntry = document.getElementById('licenseId' + licenseId);
         listEntry.remove();
       }
     });
}

function showActivity(edit) {
    if (edit === 'edit') {$('#edit-paField-modal').show();}
    else {$('#paField-modal').show();}
    document.getElementById('pa-title').value = '';
    document.getElementById('pa-title').focus();
}
function addProfessionalActivity() {
    const titleInput = document.getElementById('pa-title');
    const activityList = document.getElementById('pa-list');

    // Collect data to send asynchronously
    const server_data = [
        {attorneyId: '{{ current_attorney.id }}'},
        {title: titleInput.value}
    ];
    // Send data
    $.ajax({
       type: 'POST',
       url: "/add_activity",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function(results) {
           console.log(results);
           var activityId = results['activityId'];
           // Add the new license to the list
           const newActivity = document.createElement('li');
           newActivity.classList.add('list-entry');
           activityList.appendChild(newActivity);
           const divBullet = document.createElement('div');
           divBullet.classList.add('bullet');
           divBullet.appendChild(document.createTextNode(titleInput.value));
           newActivity.appendChild(divBullet);
           const buttonDiv = document.createElement('div');
           const editA = document.createElement('a');
           // editA.onclick =
           editA.appendChild(document.createTextNode('Edit'));
           editA.href = '#';
           editA.classList.add('button');
           buttonDiv.appendChild(editA);
           const deleteA = document.createElement('a');
           deleteA.onclick = function() { deleteActivity(activityId); };
           deleteA.appendChild(document.createTextNode('Delete'));
           deleteA.href = '#';
           deleteA.classList.add('button');
           buttonDiv.appendChild(deleteA);
           newActivity.appendChild(buttonDiv);
       }
     });
    closeModal();
}
function editActivity(activityId) {
    var activityTitle = document.getElementById('pa-title-edit');
    const server_data = [
        {activityId: activityId},
        {newTitle: activityTitle.value}
    ];
    $.ajax({
       type: "POST",
       url: "/edit_activity",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function(result) {
         console.log(result);
       }
     });
    closeModal();
}
function deleteActivity(activityId) {
    const server_data = [
        {activityId: activityId}
    ];
    $.ajax({
       type: "POST",
       url: "/delete_license",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function() {
         console.log('deleted activity');
         const listEntry = document.getElementById('activityId' + activityId);
         listEntry.remove();
       }
     });
}

function showEducation(edit) {
    if (edit === 'edit') {$('#edit-education-modal').show();}
    else{$('#education-modal').show();}
    document.getElementById('degree').value = '';
    document.getElementById('degree').focus();
    document.getElementById('school').value = '';
    document.getElementById('year').value = '';
    document.getElementById('accolades').value = '';
}
function addEducation() {
    const degreeInput = document.getElementById('degree');
    const schoolInput = document.getElementById('school');
    const yearInput = document.getElementById('year');
    const accoladesInput = document.getElementById('accolades');
    const educationList = document.getElementById('education-list');

    // Collect data to send asynchronously
    const server_data = [
        {attorneyId: '{{ current_attorney.id }}'},
        {degree: degreeInput.value},
        {school: schoolInput.value},
        {year: yearInput.value},
        {accolades: accoladesInput.value}
    ];
    // Send data
    $.ajax({
       type: 'POST',
       url: "/add_education",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function(results) {
           console.log(results);
           var educationId = results['educationId'];
           // Add the new license to the list
           const newEducation = document.createElement('li');
           newEducation.classList.add('list-entry');
           educationList.appendChild(newEducation);
           const divBullet = document.createElement('div');
           divBullet.classList.add('bullet');
           divBullet.appendChild(document.createTextNode(results['toString']));
           newEducation.appendChild(divBullet);
           const buttonDiv = document.createElement('div');
           const editA = document.createElement('a');
           // editA.onclick =
           editA.appendChild(document.createTextNode('Edit'));
           editA.href = '#';
           editA.classList.add('button');
           buttonDiv.appendChild(editA);
           const deleteA = document.createElement('a');
           deleteA.onclick = function() { deleteEducation(educationId); };
           deleteA.appendChild(document.createTextNode('Delete'));
           deleteA.href = '#';
           deleteA.classList.add('button');
           buttonDiv.appendChild(deleteA);
           newEducation.appendChild(buttonDiv);
       }
     });
    closeModal();
}
function editEducation(educationId) {
    const server_data = [
        {educationId: educationId},
        {degree: document.getElementById('degree-edit').value},
        {school: document.getElementById('publication-school-edit').value},
        {year: document.getElementById('degree-edit').value},
        {accolades: document.getElementById('accolades-edit').value}
    ];
    $.ajax({
       type: "POST",
       url: "/edit_activity",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function(result) {
         console.log(result);
       }
     });
    closeModal();
}
function deleteEducation(educationId) {
    const server_data = [
        {educationId: educationId}
    ];
    $.ajax({
       type: "POST",
       url: "/delete_education",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function() {
         console.log('deleted education');
         const listEntry = document.getElementById('educationId' + educationId);
         listEntry.remove();
       }
     });
}

function showPublication(edit) {
    if (edit === 'edit') {$('#edit-publicationField-modal').show();}
    else {$('#publicationField-modal').show();}
    document.getElementById('publication-title').value = '';
    document.getElementById('publication-title').focus();
    document.getElementById('publication-details').value = '';
    document.getElementById('publication-publication').value = '';
    document.getElementById('publication-year').value = '';
}
function addPublication() {
    const titleInput = document.getElementById('publication-title');
    const detailsInput = document.getElementById('publication-details');
    const publicationInput = document.getElementById('publication-publication');
    const yearInput = document.getElementById('publication-year');
    const publicationList = document.getElementById('publication-list');

    // Collect data to send asynchronously
    const server_data = [
        {attorneyId: '{{ current_attorney.id }}'},
        {title: titleInput.value},
        {details: detailsInput.value},
        {publication: publicationInput.value},
        {year: yearInput.value}
    ];
    // Send data
    $.ajax({
       type: 'POST',
       url: "/add_publication",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function(results) {
           console.log(results);
           var publicationString = results['toString'];
           var publicationId = results['publicationId'];
           // Add the new publication to the list
           const newPublication = document.createElement('li');
           newPublication.classList.add('list-entry');
           publicationList.appendChild(newPublication);
           const divBullet = document.createElement('div');
           divBullet.classList.add('bullet');
           divBullet.appendChild(document.createTextNode(publicationString));
           newPublication.appendChild(divBullet);
           const buttonDiv = document.createElement('div');
           const editA = document.createElement('a');
           // editA.onclick =
           editA.appendChild(document.createTextNode('Edit'));
           editA.href = '#';
           editA.classList.add('button');
           buttonDiv.appendChild(editA);
           const deleteA = document.createElement('a');
           deleteA.onclick = function() { deletePublication(publicationId); };
           deleteA.appendChild(document.createTextNode('Delete'));
           deleteA.href = '#';
           deleteA.classList.add('button');
           buttonDiv.appendChild(deleteA);
           newPublication.appendChild(buttonDiv);
       }
     });
    closeModal();
}
function editPublication(publicationId) {
    const server_data = [
        {publicationId: publicationId},
        {title: document.getElementById('publication-title-edit').value},
        {details: document.getElementById('publication-details-edit').value},
        {year: document.getElementById('publication-year-edit').value},
        {publication: document.getElementById('publication-publication-edit').value}
    ];
    $.ajax({
       type: "POST",
       url: "/edit_activity",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function(result) {
         console.log(result);
       }
     });
    closeModal();
}
function deletePublication(publicationId) {
    const server_data = [
        {publicationId: publicationId}
    ];
    $.ajax({
       type: "POST",
       url: "/delete_publication",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function() {
         console.log('deleted publication');
         const listEntry = document.getElementById('publicationId' + publicationId);
         listEntry.remove();
       }
     });
}

function showAop(edit) {
    if (edit === 'edit') {$('#edit-aopField-modal').show();}
    else {$('#aopField-modal').show();}
    document.getElementById('aop-title').value = '';
    document.getElementById('aop-title').focus();
}
function addAop() {
    const titleInput = document.getElementById('aop-title');
    const aopList = document.getElementById('aop-list');

    // Collect data to send asynchronously
    const server_data = [
        {attorneyId: '{{ current_attorney.id }}'},
        {title: titleInput.value}
    ];
    // Send data
    $.ajax({
       type: 'POST',
       url: "/add_aop",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function(results) {
           console.log(results);
           var aopId = results['aopId'];
           // Add the new license to the list
           const newAop = document.createElement('li');
           newAop.classList.add('list-entry');
           aopList.appendChild(newAop);
           const divBullet = document.createElement('div');
           divBullet.classList.add('bullet');
           divBullet.appendChild(document.createTextNode(titleInput.value));
           newAop.appendChild(divBullet);
           const buttonDiv = document.createElement('div');
           const editA = document.createElement('a');
           // editA.onclick =
           editA.appendChild(document.createTextNode('Edit'));
           editA.href = '#';
           editA.classList.add('button');
           buttonDiv.appendChild(editA);
           const deleteA = document.createElement('a');
           deleteA.onclick = function() { deleteAop(aopId); };
           deleteA.appendChild(document.createTextNode('Delete'));
           deleteA.href = '#';
           deleteA.classList.add('button');
           buttonDiv.appendChild(deleteA);
           newAop.appendChild(buttonDiv);
       }
     });
    closeModal();
}
function editAop(aopId) {
     const server_data = [
        {aopId: aopId},
        {newTitle: document.getElementById('aop-title-edit').value},
    ];
    $.ajax({
       type: "POST",
       url: "/edit_aop",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function(result) {
         console.log(result);
       }
     });
    closeModal();
}
function deleteAop(aopId) {
    const server_data = [
        {aopId: aopId}
    ];
    $.ajax({
       type: "POST",
       url: "/delete_aop",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function() {
         console.log('deleted aop');
         const listEntry = document.getElementById('aopId' + aopId);
         listEntry.remove();
       }
     });
}

function showAdmission(edit) {
    if (edit === 'edit') {$('#edit-admissionField-modal').show();}
    else{$('#admissionField-modal').show();}
    document.getElementById('admission-court').value = '';
    document.getElementById('admission-court').focus();
    document.getElementById('admission-year').value = '';
}
function addAdmission()  {
    const courtInput = document.getElementById('admission-court');
    const yearInput = document.getElementById('admission-year');
    const admissionList = document.getElementById('admission-list');

    // Collect data to send asynchronously
    const server_data = [
        {attorneyId: '{{ current_attorney.id }}'},
        {court: courtInput.value},
        {year: yearInput.value}
    ];
    // Send data
    $.ajax({
       type: 'POST',
       url: "/add_admission",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function(results) {
           console.log(results);
           var admissionId = results['admissionId'];
           var admissionString = results['toString'];
           // Add the new license to the list
           const newAdmission = document.createElement('li');
           newAdmission.classList.add('list-entry');
           admissionList.appendChild(newAdmission);
           const divBullet = document.createElement('div');
           divBullet.classList.add('bullet');
           divBullet.appendChild(document.createTextNode(admissionString));
           newAdmission.appendChild(divBullet);
           const buttonDiv = document.createElement('div');
           const editA = document.createElement('a');
           // editA.onclick =
           editA.appendChild(document.createTextNode('Edit'));
           editA.href = '#';
           editA.classList.add('button');
           buttonDiv.appendChild(editA);
           const deleteA = document.createElement('a');
           deleteA.onclick = function() { deleteAdmission(admissionId); };
           deleteA.appendChild(document.createTextNode('Delete'));
           deleteA.href = '#';
           deleteA.classList.add('button');
           buttonDiv.appendChild(deleteA);
           newAdmission.appendChild(buttonDiv);
       }
     });
    closeModal();
}
function editAdmission(admissionId) {
    const server_data = [
        {admissionId: admissionId},
        {court: document.getElementById('admission-court-edit')},
        {year: document.getElementById('admission-year-edit').value},
    ];
    $.ajax({
       type: "POST",
       url: "/edit_admission",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function(result) {
         console.log(result);
       }
     });
    closeModal();
}
function deleteAdmission(admissionId) {
    const server_data = [
        {admissionId: admissionId}
    ];
    $.ajax({
       type: "POST",
       url: "/delete_admission",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function() {
         console.log('deleted admission');
         const listEntry = document.getElementById('admissionId' + admissionId);
         listEntry.remove();
       }
     });
}

function showMembership(edit) {
    if (edit === 'edit') {$('#edit-membershipField-modal').show();}
    else{$('#membershipField-modal').show();}
    document.getElementById('membership-name').value = '';
    document.getElementById('membership-name').focus();
}
function addMembership() {
    const membershipList = document.getElementById('membership-list');

    // Collect data to send asynchronously
    const server_data = [
        {attorneyId: '{{ current_attorney.id }}'},
        {name: document.getElementById('membership-name').value}
    ];
    // Send data
    $.ajax({
       type: 'POST',
       url: "/add_membership",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function(results) {
           console.log(results);
           var membershipId = results['membershipId'];
           var membershipString = results['toString'];
           // Add the new license to the list
           const newMembership = document.createElement('li');
           newMembership.classList.add('list-entry');
           membershipList.appendChild(newMembership);
           const divBullet = document.createElement('div');
           divBullet.classList.add('bullet');
           divBullet.appendChild(document.createTextNode(membershipString));
           newMembership.appendChild(divBullet);
           const buttonDiv = document.createElement('div');
           const editA = document.createElement('a');
           // editA.onclick =
           editA.appendChild(document.createTextNode('Edit'));
           editA.href = '#';
           editA.classList.add('button');
           buttonDiv.appendChild(editA);
           const deleteA = document.createElement('a');
           deleteA.onclick = function() { deleteMembership(membershipId); };
           deleteA.appendChild(document.createTextNode('Delete'));
           deleteA.href = '#';
           deleteA.classList.add('button');
           buttonDiv.appendChild(deleteA);
           newMembership.appendChild(buttonDiv);
       }
     });
    closeModal();
}
function editMembership(membershipId) {
    const server_data = [
        {membershipId: membershipId},
        {name: document.getElementById('membership-name-edit').value},
    ];
    $.ajax({
       type: "POST",
       url: "/edit_membership",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function(result) {
         console.log(result);
       }
     });
    closeModal();
}
function deleteMembership(membershipId) {
    const server_data = [
        {membershipId: membershipId}
    ];
    $.ajax({
       type: "POST",
       url: "/delete_membership",
       data: JSON.stringify(server_data),
       contentType: "application/json",
       dataType: 'json',
       success: function() {
         console.log('deleted membership');
         const listEntry = document.getElementById('membershipId' + membershipId);
         listEntry.remove();
       }
     });
}