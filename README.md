# github-traffic-retention

```yaml
oc apply -f - <<EOF
kind: CronJob
apiVersion: batch/v1
metadata:
  name: traffic-export-llm-judge
spec:
  schedule: 0 0 */14 * *
  concurrencyPolicy: Allow
  suspend: false
  jobTemplate:
    spec:
      template:
        spec:
          restartPolicy: OnFailure
          serviceAccountName: judgeit-traffic-app-sa
          schedulerName: default-scheduler
          terminationGracePeriodSeconds: 30
          securityContext: {}
          containers:
            - resources: {}
              terminationMessagePath: /dev/termination-log
              name: run-job
              command:
                - python3
                - app.py
              env:
                - name: MONGO_DATABASE_NAME
                  valueFrom:
                    secretKeyRef:
                      name: traffic-job-secret
                      key: MONGO_DATABASE_NAME
                - name: MONGO_PASS
                  valueFrom:
                    secretKeyRef:
                      name: traffic-job-secret
                      key: MONGO_PASS
                - name: MONGO_URL
                  valueFrom:
                    secretKeyRef:
                      name: traffic-job-secret
                      key: MONGO_URL
                - name: MONGO_USER
                  valueFrom:
                    secretKeyRef:
                      name: traffic-job-secret
                      key: MONGO_USER
                - name: TRAFFIC_ACTION_OWNER
                  valueFrom:
                    secretKeyRef:
                      name: traffic-job-secret
                      key: TRAFFIC_ACTION_OWNER
                - name: TRAFFIC_ACTION_REPO
                  valueFrom:
                    secretKeyRef:
                      name: traffic-job-secret
                      key: TRAFFIC_ACTION_REPO
                - name: TRAFFIC_ACTION_TOKEN
                  valueFrom:
                    secretKeyRef:
                      name: traffic-job-secret
                      key: TRAFFIC_ACTION_TOKEN
              imagePullPolicy: IfNotPresent
              volumeMounts:
                - name: mongodb-cert-secret
                  readOnly: true
                  mountPath: /app/backend/cert
              terminationMessagePolicy: File
              image: image-registry.openshift-image-registry.svc:5000/llm-judge/traffic_retention_judgeit:11102024-v1
          serviceAccount: judgeit-traffic-app-sa
          volumes:
            - name: mongodb-cert-secret
              secret:
                secretName: mongodb-cert-secret
                defaultMode: 420
EOF
```
