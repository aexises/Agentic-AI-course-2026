# Optional Lab 17: fine-tuning investigation

This is an optional project brief, not a required executed notebook. Complete the retrieval and evaluation labs first. No GPU training has been validated as part of this course revision.

Choose a small open-weight model and a task with a reproducible scoring rule. Compare the unchanged model, a prompt-only baseline and a parameter-efficient adaptation under the same frozen held-out protocol. Separate training/development/test examples before generating or editing them; check for duplicate and near-duplicate leakage. Record model/data licenses, revisions, hardware, memory, package versions, hyperparameters, random seeds and training cost. Do not select an improvement on the test set.

First reproduce a current official training example compatible with your own GPU, then explain what LoRA trains and what quantization changes. Treat a successful import, synthetic loss curve or configuration file as setup evidence, not a completed training run. Report failures and a negative result honestly.

Deliver a runnable notebook, adapter/configuration artifacts where redistribution is permitted, a matched evaluation table and a decision about whether adaptation is justified. This optional extension does not affect offline course completion or replace the advanced capstone's live evidence requirement. Choose and verify exact current dependencies when starting; this brief intentionally makes no claim of tested training support.
