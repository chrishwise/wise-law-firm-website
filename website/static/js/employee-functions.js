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

        function showLicense(edit='', title='', id='') {
            if (edit === 'edit') {
                document.getElementById('licenseHiddenId').value = id;
                document.getElementById('pl-title-edit').value = title;
                $('#edit-plField-modal').show();
                document.getElementById('pl-title-edit').focus();
            }
            else {
                document.getElementById('pl-title').value = '';
                $('#plField-modal').show();
                document.getElementById('pl-title').focus();
            }
        }
        function addLicense() {
            const titleInput = document.getElementById('pl-title');
            const licenseList = document.getElementById('pl-list');

            // Collect data to send asynchronously
            const server_data = [
                {attorneyId: attorneyId},
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
                   editA.onclick = function() {
                       showLicense('edit', titleInput.value, licenseId);
                   }
                   editA.id='licenseEditButton' + licenseId;
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
        function editLicense(){
            var id = document.getElementById('licenseHiddenId').value;
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
               success: function(results) {
                   console.log(results);
                   const licenseString = results['toString'];
                   const licenseId = results['licenseId'];
                   const bulletDiv = document.getElementById(`licenseId${licenseId}`).firstElementChild;
                   bulletDiv.textContent = licenseString;
                   const editA = document.getElementById('licenseEditButton'+licenseId);
                   editA.onclick = function() {
                        showLicense('edit', results['title'], licenseId);
                   }
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

        function showActivity(edit='', title='', activityId='') {
            if (edit === 'edit') {
                document.getElementById('activityHiddenId').value = activityId;
                document.getElementById('pa-title-edit').value = title;
                $('#edit-paField-modal').show();
                document.getElementById('pa-title-edit').focus();
            }
            else {
                document.getElementById('pa-title').value = '';
                $('#paField-modal').show();
                document.getElementById('pa-title').focus();
            }
        }
        function addProfessionalActivity() {
            const titleInput = document.getElementById('pa-title');
            const activityList = document.getElementById('pa-list');

            // Collect data to send asynchronously
            const server_data = [
                {attorneyId: attorneyId},
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
                   newActivity.id = 'activityId' + activityId;
                   activityList.appendChild(newActivity);
                   const divBullet = document.createElement('div');
                   divBullet.classList.add('bullet');
                   divBullet.appendChild(document.createTextNode(titleInput.value));
                   newActivity.appendChild(divBullet);
                   const buttonDiv = document.createElement('div');
                   const editA = document.createElement('a');
                   editA.onclick = function() {
                       showActivity('edit', titleInput.value, activityId);
                   };
                   editA.id = 'activityEditButton' + activityId;
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
        function editActivity() {
            var activityId = document.getElementById('activityHiddenId').value;
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
               success: function(results) {
                   console.log(results);
                   const activityString = results['toString'];
                   const activityId = results['activityId'];
                   const bulletDiv = document.getElementById(`activityId${activityId}`).firstElementChild;
                   bulletDiv.textContent = activityString;
                   const editA = document.getElementById(`activityEditButton${activityId}`);
                   editA.onclick = function() {
                        showActivity('edit', results['activityTitle'], activityId);
                   }
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
               url: "/delete_activity",
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

        function showEducation(edit='', degree='', school='', year='', accolades='', id='') {
            if (edit === 'edit') {
                document.getElementById('educationHiddenId').value = id;
                document.getElementById('degree-edit').value = degree;
                document.getElementById('school-edit').value = school;
                document.getElementById('year-edit').value = year;
                document.getElementById('accolades-edit').value = accolades;
                $('#edit-education-modal').show();
                document.getElementById('degree-edit').focus();
            }
            else{
                document.getElementById('school').value = '';
                document.getElementById('year').value = '';
                document.getElementById('accolades').value = '';
                document.getElementById('degree').value = '';
                $('#education-modal').show();
                document.getElementById('degree').focus();
            }

        }
        function addEducation() {
            const degreeInput = document.getElementById('degree');
            const schoolInput = document.getElementById('school');
            const yearInput = document.getElementById('year');
            const accoladesInput = document.getElementById('accolades');
            const educationList = document.getElementById('education-list');

            // Collect data to send asynchronously
            const server_data = [
                {attorneyId: attorneyId},
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
                   // Add the new education to the list
                   const newEducation = document.createElement('li');
                   newEducation.classList.add('list-entry');
                   newEducation.id = 'educationId' + educationId;     // unique id needed for delete functionality
                   educationList.appendChild(newEducation);
                   const divBullet = document.createElement('div');
                   divBullet.classList.add('bullet');
                   divBullet.appendChild(document.createTextNode(results['toString']));
                   newEducation.appendChild(divBullet);
                   const buttonDiv = document.createElement('div');
                   const editA = document.createElement('a');
                   editA.onclick = function() {
                       showEducation('edit', results['degree'], results['school'], results['year'], results['accolades'],
                       educationId)
                   }
                   editA.id='educationEditButton' + educationId;
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
        function editEducation() {
            var educationId = document.getElementById('educationHiddenId').value;
            console.log(`educationId: ${educationId}`);
            const server_data = [
                {educationId: educationId},
                {degree: document.getElementById('degree-edit').value},
                {school: document.getElementById('school-edit').value},
                {year: document.getElementById('year-edit').value},
                {accolades: document.getElementById('accolades-edit').value}
            ];
            $.ajax({
               type: "POST",
               url: "/edit_education",
               data: JSON.stringify(server_data),
               contentType: "application/json",
               dataType: 'json',
               success: function(results) {
                 console.log(results);
                 const educationString = results['toString'];
                 const bulletDiv = document.getElementById(`educationId${educationId}`).firstElementChild;
                 bulletDiv.textContent = educationString;
                 const editA = document.getElementById('educationEditButton'+educationId);
                 editA.onclick = function() {
                     showEducation('edit', results['degree'], results['school'], results['year'], results['accolades'],
                         educationId);
                 }
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

        function showPublication(edit='', title='', details='', publication='', year='', id='') {
            if (edit === 'edit') {
                document.getElementById('publication-title-edit').value = title;
                document.getElementById('publication-details-edit').value = details;
                document.getElementById('publication-publication-edit').value = publication;
                document.getElementById('publication-year-edit').value = year;
                document.getElementById('publicationHiddenId').value = id;
                console.log("id: " + id);
                console.log(id);
                $('#edit-publicationField-modal').show();
                document.getElementById('publication-title-edit').focus();
            }
            else {
                document.getElementById('publication-title').value = '';
                document.getElementById('publication-details').value = '';
                document.getElementById('publication-publication').value = '';
                document.getElementById('publication-year').value = '';
                $('#publicationField-modal').show();
                document.getElementById('publication-title').focus();
            }
        }
        function addPublication() {
            const titleInput = document.getElementById('publication-title');
            const detailsInput = document.getElementById('publication-details');
            const publicationInput = document.getElementById('publication-publication');
            const yearInput = document.getElementById('publication-year');
            const publicationList = document.getElementById('publication-list');

            // Collect data to send asynchronously
            const server_data = [
                {attorneyId: attorneyId},
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
                   newPublication.id = 'publicationId' + publicationId;     // unique id needed for delete functionality
                   publicationList.appendChild(newPublication);
                   const divBullet = document.createElement('div');
                   divBullet.classList.add('bullet');
                   divBullet.appendChild(document.createTextNode(publicationString));
                   newPublication.appendChild(divBullet);
                   const buttonDiv = document.createElement('div');
                   const editA = document.createElement('a');
                   editA.onclick = function () {
                       showPublication('edit', results['title'], results['details'],
                           results['publication'], results['year'], publicationId);
                   }
                   editA.id = 'publicationEditButton' + publicationId;
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
        function editPublication() {
            var publicationId = document.getElementById('publicationHiddenId').value;
            var publicationList = $('#publication-list');
            const server_data = [
                {publicationId: publicationId},
                {title: document.getElementById('publication-title-edit').value},
                {details: document.getElementById('publication-details-edit').value},
                {year: document.getElementById('publication-year-edit').value},
                {publication: document.getElementById('publication-publication-edit').value}
            ];
            $.ajax({
               type: "POST",
               url: "/edit_publication",
               data: JSON.stringify(server_data),
               contentType: "application/json",
               dataType: 'json',
               success: function(results) {
                 console.log(results);
                 const publicationString = results['toString'];
                 const bulletDiv = document.getElementById(`publicationId${publicationId}`).firstElementChild;
                 bulletDiv.textContent = publicationString;

                 const editA = document.getElementById('publicationEditButton'+publicationId);
                 editA.onclick = function() {
                     showPublication('edit', results['title'], results['details'], results['publication'],
                         results['year'], publicationId);
                 }
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

        function showAop(edit='', name='', id='') {
            console.log('show aop ran');
            if (edit === 'edit') {
                document.getElementById('aopHiddenId').value = id;
                document.getElementById('aop-name-edit').value = name;
                $('#edit-aopField-modal').show();
                document.getElementById('aop-name-edit').focus();
            }
            else {
                document.getElementById('aop-name').value = '';
                $('#aopField-modal').show();
                document.getElementById('aop-name').focus();
            }
        }
        function addAop() {
            const nameInput = document.getElementById('aop-name');
            const aopList = document.getElementById('aop-list');

            // Collect data to send asynchronously
            const server_data = [
                {attorneyId: attorneyId},
                {name: nameInput.value}
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
                   console.log(aopId);
                   // Add the new license to the list
                   const newAop = document.createElement('li');
                   newAop.classList.add('list-entry');
                   newAop.id = 'aopId' + aopId;     // unique id needed for delete functionality
                   aopList.appendChild(newAop);
                   const divBullet = document.createElement('div');
                   divBullet.classList.add('bullet');
                   divBullet.appendChild(document.createTextNode(nameInput.value));
                   newAop.appendChild(divBullet);
                   const buttonDiv = document.createElement('div');
                   const editA = document.createElement('a');
                   editA.onclick = function() {
                       showAop('edit', results['aopName'], aopId);
                   };
                   editA.id = 'aopEditButton' + aopId;
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
        function editAop() {
            var aopId = document.getElementById('aopHiddenId').value;
             const server_data = [
                {aopId: aopId},
                {newName: document.getElementById('aop-name-edit').value},
            ];
            $.ajax({
               type: "POST",
               url: "/edit_aop",
               data: JSON.stringify(server_data),
               contentType: "application/json",
               dataType: 'json',
               success: function(results) {
                   console.log('results')
                   console.log(results);
                   const aopId = results['aopId'];
                   const bulletDiv = document.getElementById(`aopId` + aopId).firstElementChild;
                   bulletDiv.textContent = results['name'];
                   const editA = document.getElementById('aopEditButton'+aopId);
                   editA.onclick = function() {
                        showAop('edit', results['name'], aopId);
                   }
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

        function showAdmission(edit='', court='', year='', id='') {
            if (edit === 'edit') {
                console.log('edit ran');
                document.getElementById('admissionHiddenId').value = id;
                document.getElementById('admission-court-edit').value = court;
                document.getElementById('admission-year-edit').value = year;
                $('#edit-admissionField-modal').show();
                $('#admission-court-edit').focus();
            }
            else{
                document.getElementById('admission-court').value = '';
                document.getElementById('admission-year').value = '';
                $('#admissionField-modal').show();
                document.getElementById('admission-court').focus();

            }
        }
        function addAdmission()  {
            const courtInput = document.getElementById('admission-court');
            const yearInput = document.getElementById('admission-year');
            const admissionList = document.getElementById('admission-list');

            // Collect data to send asynchronously
            const server_data = [
                {attorneyId: attorneyId},
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
                   newAdmission.id = 'admissionId' + admissionId;     // unique id needed for delete functionality
                   admissionList.appendChild(newAdmission);
                   const divBullet = document.createElement('div');
                   divBullet.classList.add('bullet');
                   divBullet.appendChild(document.createTextNode(admissionString));
                   newAdmission.appendChild(divBullet);
                   const buttonDiv = document.createElement('div');
                   const editA = document.createElement('a');
                   editA.onclick = function() {
                       showAdmission('edit', results['admissionCourt'], results['admissionYear'], admissionId)
                   }
                   editA.id = 'admissionEditButton' + admissionId;
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
        function editAdmission() {
            var admissionId = document.getElementById('admissionHiddenId').value;
            const server_data = [
                {admissionId: admissionId},
                {court: document.getElementById('admission-court-edit').value},
                {year: document.getElementById('admission-year-edit').value},
            ];
            $.ajax({
               type: "POST",
               url: "/edit_admission",
               data: JSON.stringify(server_data),
               contentType: "application/json",
               dataType: 'json',
               success: function(results) {
                 console.log(results);
                 const admissionString = results['toString'];
                 const bulletDiv = document.getElementById(`admissionId${admissionId}`).firstElementChild;
                 bulletDiv.textContent = admissionString;
                 const editA = document.getElementById('admissionEditButton'+admissionId);
                 editA.onclick = function() {
                     showAdmission('edit', results['title'], admissionId);
                 }
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

        function showMembership(edit='', name='', id='') {
            if (edit === 'edit') {
                document.getElementById('membershipHiddenId').value = id;
                document.getElementById('membership-name-edit').value = name;
                $('#edit-membershipField-modal').show();
                document.getElementById('membership-name-edit').focus();
            }
            else{
                document.getElementById('membership-name').value = '';
                $('#membershipField-modal').show();
                document.getElementById('membership-name').focus();
            }
        }
        function addMembership() {
            const membershipList = document.getElementById('membership-list');

            // Collect data to send asynchronously
            const server_data = [
                {attorneyId: attorneyId },
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
                   newMembership.id = 'membershipId' + membershipId;     // unique id needed for delete functionality
                   membershipList.appendChild(newMembership);
                   const divBullet = document.createElement('div');
                   divBullet.classList.add('bullet');
                   divBullet.appendChild(document.createTextNode(membershipString));
                   newMembership.appendChild(divBullet);
                   const buttonDiv = document.createElement('div');
                   const editA = document.createElement('a');
                   editA.onclick = function () {
                       showMembership('edit', membershipString, membershipId);
                   };
                   editA.id = 'editMembershipButton' + membershipId;
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
        function editMembership() {
            var membershipId = document.getElementById('membershipHiddenId').value;
            console.log('membershipHiddenId: ' + membershipId);
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
               success: function(results) {
                   console.log(results);
                   const membershipName = results['toString'];
                   const bulletDiv = document.getElementById(`membershipId${membershipId}`).firstElementChild;
                   console.log(bulletDiv);
                   bulletDiv.textContent = membershipName;
                   const editA = document.getElementById('membershipEditButton'+membershipId);
                   editA.onclick = function() {
                       showMembership('edit', results['title'], membershipId);
                 }
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
