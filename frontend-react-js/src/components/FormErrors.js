import './FormErrors.css';
import FormErrorItem from './FormErrorItem';

export default function FormErrors(props) {
  const errors = props.errors || [];

  if (errors.length === 0) {
    return <div className="errors_stub" />;
  }

  return (
    <div className="errors">
      {errors.map((err_code, index) => (
        <FormErrorItem key={err_code || index} err_code={err_code} />
      ))}
    </div>
  );
}