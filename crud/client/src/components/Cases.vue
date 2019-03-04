<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Cases</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.xcase-modal>Create</button>
        <br><br>

        <!-- xcases table -->
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Case ID</th>
              <th scope="col">Subject</th>
              <th scope="col">Dossier</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(xcase, index) in xcases" :key="index">
              <td>{{ xcase.case_id }}</td>
              <td>{{ xcase.subject }}</td>
              <td>{{ xcase.dossier }}</td>
              <td>
                <button type="button"
                        class="btn btn-warning btn-sm"
                        v-b-modal.xcase-update-modal
                        @click="editCase(xcase)">
                    Update
                </button>
                <button type="button"
                        class="btn btn-danger btn-sm"
                        @click="onDeleteCase(xcase)">
                    Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>

      </div>
    </div>

    <!-- add xcase modal -->
    <b-modal ref="addCaseModal"
             id="xcase-modal"
            title="Add a new case"
            hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
        <b-form-group id="form-xcase-id-group"
                      label="Case ID:"
                      label-for="form-xcase-id-input">
            <b-form-input id="form-xcase-id-input"
                          type="text"
                          v-model="addCaseForm.case_id"
                          required
                          placeholder="Enter Case ID">
            </b-form-input>
        </b-form-group>
        <b-form-group id="form-subject-group"
                      label="Subject:"
                      label-for="form-subject-input">
          <b-form-input id="form-subject-input"
                        type="text"
                        v-model="addCaseForm.subject"
                        required
                        placeholder="Enter Subject's Name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-dossier-group"
                      label="Dossier Link:"
                      label-for="form-dossier-input">
          <b-form-input id="form-dossier-input"
                        type="text"
                        v-model="addCaseForm.dossier"
                        placeholder="Existing Dossier Link">
          </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>

    <b-modal ref="editCaseModal"
             id="xcase-update-modal"
             title="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
        <b-form-group id="form-xcase-id-edit-group"
                      label="Case ID:"
                      label-for="form-xcase-id-edit-input">
          <b-form-input id="form-xcase-id-edit-input"
                        type="text"
                        v-model="editForm.case_id"
                        required
                        placeholder="Enter Case ID">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-subject-edit-group"
                      label="Subject:"
                      label-for="form-subject-edit-input">
          <b-form-input id="form-subject-edit-input"
                        type="text"
                        v-model="editForm.subject"
                        required
                        placeholder="Enter Subject's Name">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-dossier-edit-group"
                      label="Dossier Link:"
                      label-for="form-dossier-edit-input">
          <b-form-input id="form-dossier-edit-input"
                        type="text"
                        v-model="editForm.dossier"
                        required
                        placeholder="Existing Dossier Link">
          </b-form-input>
        </b-form-group>
        <b-button type="submit" variant="primary">Update</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert';

export default {
  data() {
    return {
      cases: [],
      addCaseForm: {
        case_id: '',
        subject: '',
        dossier: '',
      },
      editForm: {
        case_id: '',
        subject: '',
        dossier: '',
      },
      message: '',
      showMessage: false,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getCases() {
      const path = 'http://localhost:5000/cases';
      axios.get(path)
        .then((res) => {
          this.cases = res.data.cases;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addCase(payload) {
      const path = 'http://localhost:5000/cases';
      axios.post(path, payload)
        .then(() => {
          this.getCases();
          this.message = 'Case created or overwritten.!!!!1';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getCases();
        });
    },
    updateCase(payload, caseID) {
      const path = `http://localhost:5000/cases/${caseID}`;
      axios.put(path, payload)
        .then(() => {
          this.getCases();
          this.message = 'Case updated.';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getCases();
        });
    },
    removeCase(caseID) {
      const path = `http://localhost:5000/cases/${caseID}`;
      axios.delete(path)
        .then(() => {
          this.getCases();
          this.message = 'Case deleted.';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getCases();
        });
    },
    initForm() {
      this.addCaseForm.case_id = '';
      this.addCaseForm.subject = '';
      this.addCaseForm.dossier = '';
      this.editForm.case_id = '';
      this.editForm.subject = '';
      this.editForm.dossier = '';
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addCaseModal.hide();
      const payload = {
        case_id: this.addCaseForm.case_id,
        subject: this.addCaseForm.subject,
        dossier: this.addCaseForm.dossier,
      };
      this.addCase(payload);
      this.initForm();
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editCaseModal.hide();
      const payload = {
        case_id: this.editForm.case_id,
        subject: this.editForm.subject,
        dossier: this.editForm.dossier,
      };
      this.updateCase(payload, this.editForm.case_id);
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addCaseModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editCaseModal.hide();
      this.initForm();
      this.getCases(); // why?
    },
    onDeleteCase(xcase) {
      this.removeCase(xcase.case_id);
    },
    editCase(xcase) {
      this.editForm = xcase;
    },
  },
  created() {
    this.getCases();
  },
};
</script>
