import {initializeApp} from "firebase-admin/app";
import {firestore} from "firebase-admin";
import {
  onDocumentCreated,
} from "firebase-functions/v2/firestore";
import {FieldValue} from "firebase-admin/firestore";

initializeApp();

const db = firestore();

// Update robot listing with id and timestamp
exports.updateListing = onDocumentCreated(
  "test_robots/{doc}",
  async (event) => {
    try {
      const docId = event.params.doc;
      if (!docId) {
        console.log("No data associated with listing");
        return;
      }
      db.doc(`test_robots/${docId}`).update({
        model_id: docId,
        created_at: FieldValue.serverTimestamp(),
      });
    } catch (error) {
      console.error("Error occurred while updating robot document:", error);
    }
  }
);

// Update software listing with id and timestamp
exports.updateSoftwareListing = onDocumentCreated(
  "test_software/{doc}",
  async (event) => {
    try {
      const docId = event.params.doc;
      if (!docId) {
        console.log("No data associated with listing");
        return;
      }
      db.doc(`test_software/${docId}`).update({
        version_id: docId,
        created_at: FieldValue.serverTimestamp(),
      });
    } catch (error) {
      console.error("Error occurred while updating software document:", error);
    }
  }
);

// Update trade data with id and timestamp
exports.updateTradeData = onDocumentCreated(
  "test_trades/{doc}",
  async (event) => {
    try {
      const docId = event.params.doc;
      if (!docId) {
        console.log("No data associated with listing");
        return;
      }
      db.doc(`test_trades/${docId}`).update({
        trade_id: docId,
        created_at: FieldValue.serverTimestamp(),
      });
    } catch (error) {
      console.error("Error occurred while updating trade document:", error);
    }
  }
);

//   npm run lint -- --fix
