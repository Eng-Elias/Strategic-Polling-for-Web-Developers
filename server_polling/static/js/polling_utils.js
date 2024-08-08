class PollingUtilities {

    static taskStatus = {
        FAILURE: 'FAILURE',
        PENDING: 'PENDING',
        RECEIVED: 'RECEIVED',
        RETRY: 'RETRY',
        REVOKED: 'REVOKED',
        STARTED: 'STARTED',
        SUCCESS: 'SUCCESS',
    }

    static async pollingFetchCheckForResult({
        parameters = {
            url: '',
            data: null,
            handleSuccess: (result) => {},
            finishPolling: (result) => {},
            handleError: (result) => {},
            handleMaximumRetriesError: (result) => {},
        },
        taskID,
        pollingTimeout = 5000,
        maxPollingRetries = 100,
        isReadyResultCallback = ({ status }) => status === PollingUtilities.taskStatus.SUCCESS,
        startSpinnerCallback = () => {},
        stopSpinnerCallback = () => {},
    }) {
        try {
            const response = await fetch(parameters.url, { method: 'GET' });
            const result = await response.json();

            if (isReadyResultCallback(result)) {
                stopSpinnerCallback();
                if (parameters.handleSuccess) {
                    parameters.handleSuccess(result);
                }
                if (parameters.finishPolling) {
                    parameters.finishPolling();
                }
            } else {
                if (maxPollingRetries === 0) {
                    stopSpinnerCallback();
                    if (parameters.handleMaximumRetriesError) {
                        parameters.handleMaximumRetriesError();
                    }
                    if (parameters.finishPolling) {
                        parameters.finishPolling();
                    }
                } else {
                    setTimeout(() => {
                        this.pollingFetchCheckForResult({
                            parameters,
                            taskID,
                            pollingTimeout,
                            maxPollingRetries: maxPollingRetries - 1,
                            isReadyResultCallback,
                            startSpinnerCallback,
                            stopSpinnerCallback,
                        });
                    }, pollingTimeout);
                }
            }
        } catch (error) {
            stopSpinnerCallback();
            if (parameters.handleError) {
                parameters.handleError(error);
            }
            if (parameters.finishPolling) {
                parameters.finishPolling();
            }
        }
    }

    static async pollingFetch({
        parameters = {
            url: '',
            method: 'POST',
            data: null,
            handleSuccess: (result) => {},
            finishPolling: (result) => {},
            handleError: (result) => {},
            handleMaximumRetriesError: (result) => {},
        },
        taskURL,
        checkForResultsURL,
        maxPollingRetries = 100,
        initialPollingTimeout = 5000,
        taskURLSuccessCallback,
        isReadyResultCallback = ({ status }) => status === PollingUtilities.taskStatus.SUCCESS,
        startSpinnerCallback = () => {},
        stopSpinnerCallback = () => {},
    }) {
        startSpinnerCallback();
        try {
            const taskResponse = await fetch(taskURL, { method: parameters.method, body: JSON.stringify(parameters.data) });
            const taskResult = await taskResponse.json();

            if (taskURLSuccessCallback) {
                taskURLSuccessCallback(taskResult);
            }

            if (taskResult.task_id) {
                parameters.url = `${checkForResultsURL}/${taskResult.task_id}`;
                parameters.data = null;  // Data is not needed for the GET request

                setTimeout(() => {
                    this.pollingFetchCheckForResult({
                        parameters,
                        maxPollingRetries,
                        pollingTimeout: initialPollingTimeout,
                        isReadyResultCallback,
                        startSpinnerCallback,
                        stopSpinnerCallback,
                    });
                }, initialPollingTimeout);
            } else {
                stopSpinnerCallback();
                if (parameters.handleSuccess) {
                    parameters.handleSuccess(taskResult);
                }
                if (parameters.finishPolling) {
                    parameters.finishPolling();
                }
            }
        } catch (error) {
            stopSpinnerCallback();
            if (parameters.handleError) {
                parameters.handleError(error);
            }
            if (parameters.finishPolling) {
                parameters.finishPolling();
            }
        }
    }
}
