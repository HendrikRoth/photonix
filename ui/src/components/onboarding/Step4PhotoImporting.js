import React from 'react'
import { useForm } from 'react-hook-form'
import { useStateMachine } from 'little-state-machine'
import { Stack } from '@chakra-ui/core'

import updateAction from './updateAction'
import ModalForm from '../ModalForm'
import ModalField from '../ModalField'

const Step4PhotoImporting = ({ history }) => {
  const { register, handleSubmit, errors, formState } = useForm()
  const { action, state } = useStateMachine(updateAction)

  const onImportFromAnotherPath = (e) => {
    action({ importFromAnotherPath: e.target.checked })
  }

  return (
    <ModalForm
      formState={formState}
      history={history}
      handleSubmit={handleSubmit}
      previousStep="/onboarding/step3"
      nextStep="/onboarding/step5"
    >
      <h2>Photo importing</h2>

      <div className="message">
        {state.data.storageBackend == 'Lo' &&
          state.data.storageContainsFiles && (
            <p>
              We see there are photos already in the location you selected as
              your base path. Should we continuously monitor this folder to
              detect you adding new files here in future? If not, we can set up
              another path to import new photos from.
            </p>
          )}
        {state.data.storageBackend == 'Lo' &&
          !state.data.storageContainsFiles && (
            <p>
              We don't currently see any photos in the base path you selected.
              Should we continuously monitor this folder to detect you adding
              new files here in future? If not, we can set up another path to
              import new photos from.
            </p>
          )}
        {state.data.storageBackend == 'S3' &&
          state.data.storageContainsFiles && (
            <p>
              We managed to connect to your S3-compatible storage and can see
              there are photos already in the location you selected as your base
              path. Should we continuously monitor this folder to detect you
              adding new files here in future? If not, we can set up another
              path to import new photos from.
            </p>
          )}
        {state.data.storageBackend == 'S3' &&
          !state.data.storageContainsFiles && (
            <p>
              We managed to connect to your S3-compatible storage but can't see
              any existing photos there yet. Should we continuously monitor this
              folder to detect you adding new files here in future? If not, we
              can set up another path to import new photos from.
            </p>
          )}
      </div>

      <Stack spacing={4} mb={4}>
        <ModalField
          name="watchForChanges"
          type="boolean"
          label="Monitor base path for changes?"
          register={register}
          errors={errors}
          defaultValue={state.data.watchForChanges}
        />
        <p>
          Is there another folder on this server that you intend to drop photos
          into and would like us to watch and import from?
        </p>
        <ModalField
          name="importFromAnotherPath"
          type="boolean"
          label="import from another path?"
          register={register}
          errors={errors}
          defaultValue={state.data.importFromAnotherPath}
          onChange={onImportFromAnotherPath}
        />
      </Stack>

      {state.data.importFromAnotherPath && (
        <Stack spacing={4}>
          <ModalField
            name="importPath"
            type="text"
            label="Import path"
            required={true}
            register={register}
            errors={errors}
            defaultValue={state.data.importPath}
          />
          <p>
            If you intend this import path's only job is to be a "drop zone" to
            get files into Photonix then we can keep it tidy by deleting the
            files that are here once we've sucessfully imported them.
          </p>
          <ModalField
            name="deleteAfterImport"
            type="boolean"
            label="Delete files after import?"
            register={register}
            errors={errors}
            defaultValue={state.data.deleteAfterImport}
          />
        </Stack>
      )}
    </ModalForm>
  )
}

export default Step4PhotoImporting
