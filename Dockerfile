# Imagen para desplegar StudyBot (Hugging Face Spaces u otra plataforma con Docker).
FROM python:3.12-slim

RUN useradd -m -u 1000 user
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=user app.py predictor.py studybot_model.joblib ./
COPY --chown=user templates ./templates

USER user
ENV PORT=7860
EXPOSE 7860
CMD gunicorn app:app --bind 0.0.0.0:$PORT --workers 2
