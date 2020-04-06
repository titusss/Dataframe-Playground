 <!-- Main form for adding data tables/matrices --> 
 
 <template>
  <div>
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group id="input-group-4" label="Type:" label-for="checkboxes-4">
        <b-form-radio-group v-model="form.checked" id="checkboxes-4" required>
          <b-form-radio name="table" value="RadioTable">Table</b-form-radio>
          <b-form-radio name="category" value="RadioCategory">Category</b-form-radio>
        </b-form-radio-group>
      </b-form-group>
      <b-form-group id="input-group-2" label="Title:" label-for="input-2">
        <b-form-input id="input-2" v-model="form.title" required placeholder></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-6" label="Source:" label-for="source-card">
        <b-card no-body id="source-card">
          <b-tabs card>
            <b-tab title="Upload" active>
              <b-form-group
                id="input-group-4"
                description="Upload a CSV, TSV, or Excel from your machine."
              >
                <b-form-file
                  v-model="form.source.file"
                  :state="Boolean(form.source.file)"
                  placeholder="Choose a file or drop it here..."
                  drop-placeholder="Drop file here..."
                  accept=".txt"
                ></b-form-file>
                <!-- <div class="mt-3">Selected file: {{ form.source.file ? form.source.file.name : '' }}</div> -->
              </b-form-group>
            </b-tab>
            <b-tab title="Database">
              <b-form-group
                id="input-group-3"
                description="Select a dataset from our global database."
              >
                <b-form-select id="input-3" v-model="form.source.database" :options="foods"></b-form-select>
              </b-form-group>
            </b-tab>
            <b-tab title="URL">
              <b-form-group id="input-group-1" description="Enter a valid URL to your dataset.">
                <b-form-input id="input-1" v-model="form.source.url" type="url" placeholder></b-form-input>
              </b-form-group>
            </b-tab>
            <b-tab title="Text">
              <b-form-group id="input-group-1" description="Paste comma-seperated values here.">
                <b-form-textarea
                  id="textarea"
                  v-model="form.source.text"
                  placeholder="Comma-seperated values..."
                  rows="9"
                  max-rows="10000"
                ></b-form-textarea>
              </b-form-group>
            </b-tab>
          </b-tabs>
        </b-card>
      </b-form-group>
       <b-alert v-model="showErrorAlert" variant="danger" dismissible>{{sourceErrMsg}}</b-alert>
      <pre class="mt-3 mb-0">{{ text }}</pre>
      <b-button type="submit" variant="primary">Add</b-button>
      <b-button type="reset" variant="danger" @click="$bvModal.hide('bv-modal-addData')">Cancel</b-button>
    </b-form>
  </div>
</template>


<script>
export default {
  name: "addDataForm",
  data() {
    return {
      sourceErrMsg: "",
      showErrorAlert: false,
      form: {
        title: "",
        checked: [],
        source: {
          file: null,
          database: null,
          url: null,
          text: null
        }
      },
      text: "",
      foods: [
        { text: "Select One", value: null },
        "Carrots",
        "Beans",
        "Tomatoes",
        "Corn"
      ],
      show: true
    };
  },
  methods: {
    validateForm(obj) {
      var properties = 0;
      for (var key in obj) {
        console.log(obj[key])
        if (obj[key] !== null && obj[key] !== "") {
          properties++;
        }
      }
      if (properties < 1) {
        this.sourceErrMsg = "Please enter a data-source.";
        this.showErrorAlert=true;
      }
      else if (properties > 1) {
        this.sourceErrMsg = "Please enter no more than one data-source.";
        this.showErrorAlert=true;
      }
      else {
        alert(JSON.stringify(this.form));
      }
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.validateForm(this.form.source);
    },
    onReset(evt) {
      evt.preventDefault();
      // Reset our form values
      this.form.email = "";
      this.form.name = "";
      this.form.food = null;
      this.form.checked = [];
      // Trick to reset/clear native browser form validation state
      this.show = false;
      this.$nextTick(() => {
        this.show = true;
      });
    }
  }
};
</script>