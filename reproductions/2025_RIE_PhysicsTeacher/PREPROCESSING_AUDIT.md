# Input / Preprocessing Audit — 2026-09-09

Paper: **Failure mechanism-driven multi-adversarial domain transfer learning for rolling bearing fault diagnosis**  
DOI: 10.1016/j.rineng.2025.106165

## Confirmed from the open full text

- The pre-trained model is a deep CNN trained with **simulated bearing vibration data**.
- The pre-trained feature extractor is intentionally similar to the transfer network feature extractor.
- The proposed shared feature extractor contains **4 convolutional layers + BN + CBAM**.
- The paper compares against a baseline named **CNN2d**.
- The paper gives training hyperparameters (SGD, LR, batch size, iterations, loss weights).

## Not found in the accessible full text

The open text does **not** provide a reproducible specification for:

- exact simulated-signal window length;
- overlap/stride;
- normalization formula;
- whether the proposed network receives raw 1-D vibration directly;
- whether vibration is reshaped into a 2-D array;
- whether STFT/CWT/envelope/time-frequency images are used;
- exact dimensions of the input tensor before Conv1.

The general introduction mentions that deep networks can learn from raw vibration signals **or simple transformations**, but this is background discussion and cannot be treated as the method's preprocessing specification.

The existence of a comparison baseline named CNN2d is also insufficient to prove the proposed method's exact input transformation.

## Reproduction decision

Until stronger evidence is available:

1. retain raw 64-kHz simulated windows as the canonical Teacher-pilot data;
2. do not label any 1-D/2-D transformation as PAPER-CONFIRMED;
3. keep Teacher pretraining blocked for the **paper-faithful** track;
4. if a fallback is later required, implement it under an explicitly named
   reproduction fallback config and compare alternatives rather than silently
   choosing one.

Current status: **UNRESOLVED, transparently bounded**.
