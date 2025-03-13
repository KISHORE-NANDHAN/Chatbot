const mongoose = require('mongoose');
const fs = require('fs');

const departmentSchema = new mongoose.Schema({
    name: String,
    department : [String],
    hod: String,
    courses: [String],
    faculty: [
        {
            name: String,
            designation: String,
            department: String,
            image_url : String,
            pdf_url : String,
            research_areas: [String],
            email: [String], // Fix: Convert to array
            phone: [String],
            experience: String,
            education: {
                phd: String,
                mtech: String,
                btech: String
            },
            teaching_subjects: [String],
            publications: { // Fix: Change String to Number
                journals: Number,
                conferences: Number,
                patents: Number
            },
            professional_memberships: [String],
            achievements_and_awards : [String],
            roles: [String]
        }
    ]
});

const Department = mongoose.model('Department', departmentSchema);

async function insertData() {
    try {
        await mongoose.connect('mongodb+srv://Admin:Manager@cluster0.vths3.mongodb.net/CollegeDB?retryWrites=true&w=majority', {
            useNewUrlParser: true,
            useUnifiedTopology: true
        });
        console.log('✅ Connected to MongoDB');

        // Load JSON file
        const jsonData = JSON.parse(fs.readFileSync('./db-based/All_Faculty_LBRCE.json', 'utf8'));

        // Fix department key mismatch
        await Department.insertMany(jsonData.department);

        console.log('✅ Data inserted successfully');
        mongoose.connection.close();
    } catch (error) {
        console.error('❌ Error inserting data:', error);
    }
}

insertData();
